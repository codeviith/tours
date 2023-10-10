from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string, datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)




class Patient(db.Model, SerializerMixin): ### the many
    __tablename__ = "patient_table"

    serialize_rules = ("-appointments.patient",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    doctors = association_proxy("appointments", "doctor") ### this is the same as:
    # doctor = [appointment.doctor for appointment in appointments]
    # we use association proxy so that we don't have to keep repeating ourself




class Appointment(db.Model, SerializerMixin): ### the middle --> the one
    __tablename__ = "appointment_table"

    serialize_rules = ("-patient.appointments", "-doctor.appointments")

    id = db.Column(db.Integer, primary_key=True)
    day = db.Coumn(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_table.id")) # an object
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_table.id")) # an object

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")

    @validates('day')
    def validate_appointment(self, key, day):
        days = ["Mon", "Tues", "Wed", "Thur", "Fri", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        if day not in days:
            raise ValueError("Days must be from Monday to Friday.")
        return day




class Doctor(db.Model, SerializerMixin): ### the many
    __tablename__ = "doctor_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)

    appointments = db.relationship("Appointment", back_populates="doctor")

    patients = association_proxy("appointments", "patients")

    @validates('name')
    def validate_doc_name(self, key, name):
        if not name.startswith("Dr."):
            raise ValueError("Doctor's name must have a 'Dr.' in front!")
        return name


