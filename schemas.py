from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CreateAppointmentSchema(BaseModel):
    status: str = Field(...)
    patient_id: int = Field(...)
    date: datetime = Field(...)


class ReadAppointmentSchema(BaseModel):
    id: int
    status: str
    first_name: str
    last_name: str
    age: int
    gender: str
    date: datetime


class UpdateAppointmentSchema(BaseModel):
    status: str | None = None
    date: datetime | None = None


class CreateMedicalInterview(BaseModel):
    appointment_id: int = Field(...)
    initial_consult: str = Field(None)


class UpdateMedicalInterview(BaseModel):
    initial_consult: str | None = None
    initial_findings: str | None = None
    visit_reason: str | None = None
    symptoms: str | None = None
    duration: str | None = None
    severity: str | None = None
    current_medications: str | None = None
    allergies: str | None = None

    model_config = ConfigDict(extra="forbid")
