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


class Patient(db.Model, SerializerMixin):
    __tablename__ = "patient_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    @validates('name')
    def validate_pt_name(self, key, name):
        if name != string:
            raise ValueError("Name must be a string!")
        return name


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment_table"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Coumn(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)

    @validates('day')
    def validate_appointment(self, key, day):
        days = ["Mon", "Tues", "Wed", "Thur", "Fri", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        if day not in days:
            raise ValueError("Days must be from Monday to Friday.")
        return day



class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctor_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)

    @validates('name')
    def validate_doc_name(self, key, name):
        if not "Dr." in name:
            raise ValueError("Doctor's name must have a 'Dr.' in front")
        return name


