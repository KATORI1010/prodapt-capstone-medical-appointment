import os
from typing import Annotated
import string
import random
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator
from fastapi import (
    FastAPI,
    Request,
    Response,
    HTTPException,
    UploadFile,
    Form,
    status,
    BackgroundTasks,
    Depends,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text, desc

# from supabase import create_client, Client
from openai import OpenAI

from db import get_db_session, get_db, Session
from models import Appointment, MedicalInterview
from schemas import ReadAppointmentSchema, CreateMedicalInterview
from auth import (
    authenticate_admin,
    is_admin,
    delete_admin_session,
    AdminAuthzMiddleware,
    AdminSessionMiddleware,
)
from chatkit.server import StreamingResult
from intake_chat.server import MyChatKitServer, MyRequestContext
from intake_chat.store import MyChatKitStore


from config import settings

app = FastAPI()
app.add_middleware(AdminAuthzMiddleware)
app.add_middleware(AdminSessionMiddleware)


WORKFLOW_ID = settings.WORKFLOW_ID
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class SessionReq(BaseModel):
    user: str | None = None


@app.post("/api/chatkit/session")
def create_session(req: SessionReq):
    user = req.user or "local-dev-user"
    s = client.beta.chatkit.sessions.create(
        user=user,
        workflow={"id": WORKFLOW_ID},
        # 必要なら expires_after なども後で調整可
    )
    return {"client_secret": s.client_secret}


server = MyChatKitServer(store=MyChatKitStore())


@app.post("/chatkit")
async def chatkit(request: Request, db: Session = Depends(get_db)):
    interview_id = request.headers.get("x-interview-id") or "anonymous"
    print(interview_id)
    context = MyRequestContext(db=db, interview_id=int(interview_id))

    result = await server.process(await request.body(), context=context)
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")


class AppointmentForm(BaseModel):
    status: str = Field(...)
    patient_id: int = Field(...)
    date: datetime = Field(...)


# Create Appointments
@app.post("/api/appointments")
async def api_create_appointment(
    appointment_form: Annotated[AppointmentForm, Form()], db: Session = Depends(get_db)
):
    db_appointment = Appointment(
        status=appointment_form.status,
        patient_id=appointment_form.patient_id,
        date=appointment_form.date,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# Read Appointments
# @app.get("/api/appointments")
# async def api_read_appointments(db: Session = Depends(get_db)):
#     db_appointments = db.query(Appointment).order_by(desc(Appointment.date)).all()
#     return db_appointments


@app.get("/api/appointments", response_model=list[ReadAppointmentSchema])
async def api_read_appointments(db: Session = Depends(get_db)):
    db_appointments = (
        db.query(Appointment)
        .join(Appointment.patient)
        .order_by(desc(Appointment.date))
        .all()
    )

    return [
        ReadAppointmentSchema(
            id=appointment.id,
            status=appointment.status,
            first_name=appointment.patient.first_name,
            last_name=appointment.patient.last_name,
            age=appointment.patient.age,
            gender=appointment.patient.gender,
            date=appointment.date,
        )
        for appointment in db_appointments
    ]


# Create Medical Interviews
@app.post("/api/medical_interviews")
async def api_create_medical_interviews(
    medical_interview_form: Annotated[CreateMedicalInterview, Form()],
    db: Session = Depends(get_db),
):
    db_medical_interview = MedicalInterview(
        appointment_id=medical_interview_form.appointment_id,
        initial_consult=medical_interview_form.initial_consult,
        created_at=datetime.now(),
    )
    db.add(db_medical_interview)
    db.commit()
    db.refresh(db_medical_interview)
    return db_medical_interview


# Read Medical Interviews
@app.get("/api/medical_interviews")
async def api_read_medical_interviews(
    appointment_id: int, db: Session = Depends(get_db)
):
    db_medical_interviews = (
        db.query(MedicalInterview)
        .filter(MedicalInterview.appointment_id == appointment_id)
        .order_by(desc(MedicalInterview.created_at))
        .first()
    )
    return db_medical_interviews


# Read One Medical Interviews
@app.get("/api/medical_interviews/{interview_id}")
async def api_read_medical_interview_by_id(
    interview_id: int, db: Session = Depends(get_db)
):
    db_medical_interview = db.get(MedicalInterview, interview_id)
    if not db_medical_interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical interview not found."
        )
    return db_medical_interview


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    indexFilePath = os.path.join("frontend", "build", "client", "index.html")
    return FileResponse(path=indexFilePath, media_type="text/html")
