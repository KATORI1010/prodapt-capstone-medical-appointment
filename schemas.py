from pydantic import BaseModel, Field

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
    initial_consult: str | None = Field(None)
    initial_findings: str | None = Field(None)
    visit_reason: str | None = Field(None)
    symptoms: str | None = Field(None)
    duration: str | None = Field(None)
    severity: str | None = Field(None)
    current_medications: str | None = Field(None)
    allergies: str | None = Field(None)