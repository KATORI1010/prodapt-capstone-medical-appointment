from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

# Memo
# alembic revision --autogenerate -m "add job posts"
# alembic upgrade head
# alembic downgrade -1


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    medical_interviews = relationship(
        "MedicalInterview", back_populates="appointment", cascade="all, delete-orphan"
    )


class MedicalInterview(Base):
    __tablename__ = "medical_interviews"
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    initial_consult = Column(Text, nullable=True)
    initial_findings = Column(Text, nullable=True)
    visit_reason = Column(Text, nullable=True)
    symptoms = Column(Text, nullable=True)
    duration = Column(Text, nullable=True)
    severity = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    appointment = relationship("Appointment", back_populates="medical_interviews")


# class JobApplicationAIEvaluation(Base):
#     __tablename__ = "job_application_ai_evaluations"
#     id = Column(Integer, primary_key=True)
#     job_application_id = Column(
#         Integer, ForeignKey("job_applications.id"), nullable=False
#     )
#     overall_score = Column(Integer, nullable=False)
#     evaluation = Column(JSONB, nullable=False)
