from dataclasses import dataclass

from agents import function_tool, RunContextWrapper
from chatkit.agents import AgentContext
from chatkit.types import ProgressUpdateEvent

from db import Session
from models import MedicalInterview
from schemas import UpdateMedicalInterview


@dataclass
class MyRequestContext:
    db: Session
    interview_id: int


# @dataclass
class MyAgentContext(AgentContext):
    request_context: MyRequestContext


@function_tool
async def report_progress(ctx: RunContextWrapper[MyAgentContext], text: str) -> None:
    """
    This function notifies the process to user.

    Args:
    - text: The message to notify
    """
    await ctx.context.stream(ProgressUpdateEvent(text=text))


@function_tool
def read_medical_interview(ctx: RunContextWrapper[MyAgentContext]) -> dict:
    """
    This function retrieves the medical interview form from the database
    and returns its contents.
    """
    db = ctx.context.request_context.db
    interview_id = ctx.context.request_context.interview_id

    obj = db.get(MedicalInterview, interview_id)

    return {
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


@function_tool
async def update_medical_interview(
    ctx: RunContextWrapper[MyAgentContext],
    content: UpdateMedicalInterview,
) -> dict:
    """
    This function updates the questionnaire in the database.
    It updates only the items entered as arguments.

    Args:
    - content: UpdateMedicalInterview
    """
    await ctx.context.stream(ProgressUpdateEvent(text="Updating DB Data…"))

    db = ctx.context.request_context.db
    interview_id = ctx.context.request_context.interview_id

    obj = db.get(MedicalInterview, interview_id)
    if obj is None:
        return {"ok": False, "error": "MedicalInterview not found"}

    updates = content.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)

    return {
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
