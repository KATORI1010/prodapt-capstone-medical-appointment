from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from agents import function_tool, RunContextWrapper
from chatkit.agents import AgentContext
from chatkit.types import (
    ProgressUpdateEvent,
    ClientEffectEvent,
    ClosedStatus,
)
from chatkit.widgets import WidgetTemplate

from db import Session
from models import Appointment, MedicalInterview
from schemas import UpdateMedicalInterview
from medical_agents.intake_schemas import IntakeForm, IntakeFormPatch


@dataclass
class MyRequestContext:
    db: Session
    interview_id: int


class MyAgentContext(AgentContext):
    request_context: MyRequestContext


def load_prompt_md(relative_path: str) -> str:
    base_dir = Path(__file__).resolve().parent
    prompt_path = base_dir / relative_path
    return Path(prompt_path).read_text(encoding="utf-8-sig")


@function_tool
async def report_progress(ctx: RunContextWrapper[MyAgentContext], text: str) -> None:
    """
    This function notifies the process to user.

    Args:
    - text: The message to notify (**English Only**)
    """
    # ステータスメッセージの更新 (Update status message)
    await ctx.context.stream(ProgressUpdateEvent(text=text))


@function_tool
async def report_completion(ctx: RunContextWrapper[MyAgentContext]) -> None:
    """
    This function notifies the interview completion to user.
    """
    # ステータスメッセージの更新 (Update status message)
    await ctx.context.stream(ProgressUpdateEvent(text="Review passed."))

    # MedicalInterviewとAppointmentテーブルのステータス更新
    # (Update status of MedicalInterview and Appointment table)
    db = ctx.context.request_context.db
    interview_id = ctx.context.request_context.interview_id

    db_medical_interview = db.get(MedicalInterview, interview_id)
    db_medical_interview.status = "completed"
    db_appointment = db.get(Appointment, db_medical_interview.appointment_id)
    db_appointment.status = "Ready for medical examination"
    db.commit()

    # ClientのonEffectフックへの連携 (Integration with the Client's onEffect hook)
    await ctx.context.stream(
        ClientEffectEvent(
            name="interview_completed",
            data={},
        )
    )

    # 完了を通知するWidgetを表示 (Display a widget to notify of completion)
    base_dir = Path(__file__).resolve().parent
    widget_path = base_dir / "widgets/completion_notification.widget"
    widget_template = WidgetTemplate.from_file(widget_path)

    widget = widget_template.build(
        {
            "title": "Medical interview completed",
            "description": "Notify me when this item ships",
            "buttonLabel": "Return to home",
            "url": "/?status=complete",
        }
    )
    await ctx.context.stream_widget(widget)

    # Threadのクローズ (Close the thread)
    thread = ctx.context.thread
    store = ctx.context.store
    request_context = ctx.context.request_context
    thread.status = ClosedStatus(reason="Medical interview completed.")
    await store.save_thread(thread, context=request_context)


@function_tool
def read_intake_form(ctx: RunContextWrapper[MyAgentContext]) -> dict:
    """
    This function retrieves the intake form from the database
    and returns its contents.
    """
    db = ctx.context.request_context.db
    interview_id = ctx.context.request_context.interview_id

    obj = db.get(MedicalInterview, interview_id)

    return obj.intake


@function_tool
async def update_intake_form(
    ctx: RunContextWrapper[MyAgentContext],
    patch: IntakeFormPatch,
) -> dict:
    """
    Partially updates an IntakeForm stored in a single PostgreSQL JSONB column.

    Behavior:
    - Only fields explicitly provided in `patch` will be applied.
    - Fields not provided in `patch` will remain unchanged.
    - The updated form is written back to the JSONB column as a plain dict.
    - Returns the updated JSON payload so the UI can refresh the right pane.

    Notes:
    - List fields (symptoms/medications/allergies) are replaced as a whole if provided.
      For "append one item" behavior, create separate append_* tools.
    """
    await ctx.context.stream(ProgressUpdateEvent(text="Updating intake form in DB..."))

    db = ctx.context.request_context.db
    interview_id = ctx.context.request_context.interview_id

    obj = db.get(MedicalInterview, interview_id)
    if obj is None:
        return {"ok": False, "error": "MedicalInterview not found"}

    # 1) JSONB (dict) -> Pydantic. If empty, initialize to defaults.
    current_form = IntakeForm.model_validate(obj.intake or {})

    # 2) Keep only fields actually provided by the model (PATCH semantics).
    updates = patch.model_dump(exclude_unset=True, mode="json")

    # Optional safety: ignore explicit null for list fields (treat as "no update")
    for k in ("symptoms", "medications", "allergies"):
        if k in updates and updates[k] is None:
            updates.pop(k)

    # 3) Merge and set timestamp.
    merged = current_form.model_dump(mode="json")
    merged.update(updates)
    merged["updated_at"] = datetime.utcnow().isoformat()

    # Optional safety: normalize list fields if they somehow become null
    for k in ("symptoms", "medications", "allergies"):
        if merged.get(k) is None:
            merged[k] = []

    # 4) Validate BEFORE DB write, then store dict into JSONB.
    obj.intake = IntakeForm.model_validate(merged).model_dump(mode="json")

    db.commit()
    db.refresh(obj)

    await ctx.context.stream(ProgressUpdateEvent(text="Update complete: Intake form"))

    return {
        "ok": True,
        "medical_interview": {
            "id": obj.id,
            "appointment_id": obj.appointment_id,
            "form": obj.intake,
        },
    }


# -----------------------------
# The following tools are old. These are not used now.
# -----------------------------
#
# @function_tool
# def read_medical_interview(ctx: RunContextWrapper[MyAgentContext]) -> dict:
#     """
#     This function retrieves the medical interview form from the database
#     and returns its contents.
#     """
#     db = ctx.context.request_context.db
#     interview_id = ctx.context.request_context.interview_id

#     obj = db.get(MedicalInterview, interview_id)

#     return {
#         "ok": True,
#         "medical_interview": {
#             "id": obj.id,
#             "appointment_id": obj.appointment_id,
#             "initial_consult": obj.initial_consult,
#             "initial_findings": obj.initial_findings,
#             "visit_reason": obj.visit_reason,
#             "symptoms": obj.symptoms,
#             "duration": obj.duration,
#             "severity": obj.severity,
#             "current_medications": obj.current_medications,
#             "allergies": obj.allergies,
#         },
#     }


# @function_tool
# async def update_medical_interview(
#     ctx: RunContextWrapper[MyAgentContext],
#     content: UpdateMedicalInterview,
# ) -> dict:
#     """
#     This function updates the questionnaire in the database.
#     It updates only the items entered as arguments.

#     Args:
#     - content: UpdateMedicalInterview
#     """
#     await ctx.context.stream(ProgressUpdateEvent(text="Updating DB Data…"))

#     db = ctx.context.request_context.db
#     interview_id = ctx.context.request_context.interview_id

#     obj = db.get(MedicalInterview, interview_id)
#     if obj is None:
#         return {"ok": False, "error": "MedicalInterview not found"}

#     updates = content.model_dump(exclude_unset=True)
#     for k, v in updates.items():
#         setattr(obj, k, v)

#     db.commit()
#     db.refresh(obj)

#     return {
#         "ok": True,
#         "medical_interview": {
#             "id": obj.id,
#             "appointment_id": obj.appointment_id,
#             "initial_consult": obj.initial_consult,
#             "initial_findings": obj.initial_findings,
#             "visit_reason": obj.visit_reason,
#             "symptoms": obj.symptoms,
#             "duration": obj.duration,
#             "severity": obj.severity,
#             "current_medications": obj.current_medications,
#             "allergies": obj.allergies,
#         },
#     }
