from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ReadAppointmentSchema(BaseModel):
    id: int
    status: str
    first_name: str
    last_name: str
    age: int
    gender: str
    date: datetime


class CreateMedicalInterview(BaseModel):
    appointment_id: int = Field(...)
    initial_consult: str = Field(None)
    initial_findings: str | None = Field(None)
    visit_reason: str | None = Field(None)
    symptoms: str | None = Field(None)
    duration: str | None = Field(None)
    severity: str | None = Field(None)
    current_medications: str | None = Field(None)
    allergies: str | None = Field(None)


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
