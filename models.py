import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

# Memo
# alembic revision --autogenerate -m "add job posts"
# alembic upgrade head
# alembic downgrade -1


class Genter(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender: Mapped[Genter] = mapped_column(
        Enum(
            Genter,
            name="gender",
            native_enum=True,
            validate_strings=True,
        )
    )
    appointments = relationship(
        "Appointment", back_populates="patient", cascade="all, delete-orphan"
    )


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date = Column(DateTime, nullable=True)
    patient = relationship("Patient", back_populates="appointments")
    medical_interviews = relationship(
        "MedicalInterview", back_populates="appointment", cascade="all, delete-orphan"
    )


class MedicalInterview(Base):
    __tablename__ = "medical_interviews"
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    initial_consult = Column(Text, nullable=True)
    # initial_findings = Column(Text, nullable=True)
    # visit_reason = Column(Text, nullable=True)
    # symptoms = Column(Text, nullable=True)
    # duration = Column(Text, nullable=True)
    # severity = Column(Text, nullable=True)
    # current_medications = Column(Text, nullable=True)
    # allergies = Column(Text, nullable=True)
    intake = Column(JSONB, nullable=True, default={})
    created_at = Column(DateTime, nullable=True)
    appointment = relationship("Appointment", back_populates="medical_interviews")
