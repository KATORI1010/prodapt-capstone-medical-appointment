from typing import AsyncIterator
from dotenv import load_dotenv
from dataclasses import dataclass

import truststore  # SSL証明書エラーの対応のため
from openai.types.shared import Reasoning
from agents import Agent, Runner, ModelSettings, set_trace_processors
from chatkit.server import ChatKitServer
from chatkit.types import (
    ThreadMetadata,
    UserMessageItem,
    ThreadStreamEvent,
)
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from braintrust import init_logger
from braintrust.wrappers.openai import BraintrustTracingProcessor

from config import settings

# from medical_agents.medical_interview_agent import medical_interview_agent
from medical_agents.medical_interview_agent_modifing import (
    medical_interview_agent,
    MyRequestContext,
    MyAgentContext,
)

load_dotenv()
truststore.inject_into_ssl()  # SSL証明書エラーの対応のため

class MyChatKitServer(ChatKitServer[dict]):
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: MyRequestContext,  # dictから型指定した独自クラスに変更
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Convert recent thread items (which includes the user message) to model input
        items_page = await self.store.load_thread_items(
            thread.id,
            after=None,
            limit=20,
            order="asc",
            context=context,
        )
        input_items = await simple_to_agent_input(items_page.data)

        set_trace_processors(
            [
                BraintrustTracingProcessor(
                    init_logger("Prodapt", api_key=settings.BRAINTRUST_API_KEY)
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
