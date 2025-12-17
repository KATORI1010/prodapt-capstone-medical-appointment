from db import get_db_session
from models import Patient, Appointment


with get_db_session() as db:
    db_patient = Patient(
        first_name="patient",
        last_name="1",
        age=31,
        gender="male",
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    db_appointment_1 = Appointment(
        status="closed",
        patient_id=db_patient.id,
        date="2025-11-02 11:30:00",
    )
    db_appointment_2 = Appointment(
        status="Medical interview required",
        patient_id=db_patient.id,
        date="2025-12-19 18:30:00",
    )
    db.add(db_appointment_1)
    db.add(db_appointment_2)
    db.commit()
