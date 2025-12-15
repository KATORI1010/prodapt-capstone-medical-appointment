from typing import AsyncIterator
from dotenv import load_dotenv
from dataclasses import dataclass
from datetime import datetime
import uuid

import truststore  # SSL証明書エラーの対応のため
from openai.types.shared import Reasoning
from agents import Agent, Runner, ModelSettings, set_trace_processors
from chatkit.server import ChatKitServer
from chatkit.types import (
    ThreadMetadata,
    UserMessageItem,
    HiddenContextItem,
    ThreadStreamEvent,
)
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from braintrust import init_logger
from braintrust.wrappers.openai import BraintrustTracingProcessor

from models import MedicalInterview
from config import settings

from medical_agents.tools import MyRequestContext, MyAgentContext
from medical_agents.medical_interview_agent_modifing import medical_interview_agent

load_dotenv()
truststore.inject_into_ssl()  # SSL証明書エラーの対応のため


class MyChatKitServer(ChatKitServer[dict]):
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: MyRequestContext,  # dictから型指定した独自クラスに変更
    ) -> AsyncIterator[ThreadStreamEvent]:
        db = context.db
        interview_id = context.interview_id

        obj = db.get(MedicalInterview, interview_id)

        interview_data = {
            "ok": True,
            "medical_interview": {
                "id": obj.id,
                "appointment_id": obj.appointment_id,
                "initial_consult": obj.initial_consult,
                "initial_findings": obj.initial_findings,
                "visit_reason": obj.visit_reason,
                "symptoms": obj.symptoms,
                "duration": obj.duration,
                "severity": obj.severity,
                "current_medications": obj.current_medications,
                "allergies": obj.allergies,
            },
        }

        hidden_context = HiddenContextItem(
            id=f"hc_{uuid.uuid4().hex}",
            thread_id=thread.id,
            created_at=datetime.now(),
            content=f"<MEDICAL_INTERVIEW_FORM>\n{interview_data}\n</MEDICAL_INTERVIEW_FORM>",
        )

        # Convert recent thread items (which includes the user message) to model input
        items_page = await self.store.load_thread_items(
            thread.id,
            after=None,
            limit=20,
            order="asc",
            context=context,
        )
        # input_items = await simple_to_agent_input(items_page.data)
        input_items = await simple_to_agent_input([hidden_context, *items_page.data])

        set_trace_processors(
            [
                BraintrustTracingProcessor(
                    init_logger("Capstone", api_key=settings.BRAINTRUST_API_KEY)
                )
            ]
        )

        # Stream the run through ChatKit events
        # 型指定するためにAgentContextから独自クラスに変更
        agent_context = MyAgentContext(
            thread=thread, store=self.store, request_context=context
        )
        result = Runner.run_streamed(
            medical_interview_agent, input_items, context=agent_context
        )
        async for event in stream_agent_response(agent_context, result):
            yield event
