from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patient_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Stirng, nullable=False)
    
class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointment_table'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Datetime, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctor_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Stirng, nullable=False)
    specialty = db.Column(db.String, nullable=False)

