import os
from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import (
    FastAPI,
    Request,
    Response,
    HTTPException,
    Form,
    status,
    Depends,
)
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import desc
from openai import OpenAI

from db import get_db, Session
from models import Appointment, MedicalInterview
from schemas import (
    CreateAppointmentSchema,
    ReadAppointmentSchema,
    UpdateAppointmentSchema,
    CreateMedicalInterview,
)
from chatkit.server import StreamingResult
from intake_chat.server import MyChatKitServer, MyRequestContext
from intake_chat.store import MyChatKitStore


from config import settings

app = FastAPI()

# Create session key to connect Chatkit with OpenAI Visual Builder
# Use only when using Visual Builder
# WORKFLOW_ID = settings.WORKFLOW_ID
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# class SessionReq(BaseModel):
#     user: str | None = None

# @app.post("/api/chatkit/session")
# def create_session(req: SessionReq):
#     user = req.user or "local-dev-user"
#     s = client.beta.chatkit.sessions.create(
#         user=user,
#         workflow={"id": WORKFLOW_ID},
#     )
#     return {"client_secret": s.client_secret}


server = MyChatKitServer(store=MyChatKitStore())


# Chatkit Endpoint
@app.post("/chatkit")
async def chatkit(request: Request, db: Session = Depends(get_db)):
    interview_id = request.headers.get("x-interview-id") or "anonymous"
    context = MyRequestContext(db=db, interview_id=int(interview_id))

    result = await server.process(await request.body(), context=context)
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")


# Create Appointment
@app.post("/api/appointments")
async def api_create_appointment(
    appointment_form: Annotated[CreateAppointmentSchema, Form()],
    db: Session = Depends(get_db),
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


# Update Appointment
@app.put("/api/appointments/{appointment_id}")
async def api_update_appointment(
    appointment_id: int,
    appointment_form: Annotated[UpdateAppointmentSchema, Form()],
    db: Session = Depends(get_db),
):
    db_appointment = db.get(Appointment, appointment_id)
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found."
        )
    if appointment_form.status is not None:
        db_appointment.status = appointment_form.status
    if appointment_form.date is not None:
        db_appointment.date = appointment_form.date
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# Create Medical Interviews
@app.post("/api/medical_interviews")
async def api_create_medical_interviews(
    medical_interview_form: Annotated[CreateMedicalInterview, Form()],
    db: Session = Depends(get_db),
):
    db_appointment = db.get(Appointment, medical_interview_form.appointment_id)
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found."
        )

    db_medical_interview = MedicalInterview(
        status="draft",
        appointment_id=medical_interview_form.appointment_id,
        initial_consult=medical_interview_form.initial_consult,
        created_at=datetime.now(),
        intake={
            "full_name": " ".join(
                [db_appointment.patient.first_name, db_appointment.patient.last_name]
            ),
            "age_years": db_appointment.patient.age,
            "sex": db_appointment.patient.gender,
            "initial_patient_message": medical_interview_form.initial_consult,
        },
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
