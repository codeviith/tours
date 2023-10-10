#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from models import db, Doctor, Patient, Appointment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.get("/")
def index():
    return "doctor/patient"

@app.get('/doctors')
def get_doctors():
    doctors = Doctor.query.all()
    data = [doctor.to_dict(rules=("-appointments",)) for doctor in doctors]
    return make_response(jsonify(data), 200)

@app.get('/doctors/<int:id>')
def get_doctor_by_id(id):
    #doctor = Doctor.query.filter(Doctor.id == id).first()
    doctor = db.session.get(Doctor, id)
    if not doctor:
        return make_response(jsonify({"Error": "Doctor not found"}))
    return make_response(jsonify(doctor.to_dict(rules=("-appointments.patient_id", "-appointments.doctor_id"))), 200)


@app.get('/patients/<int:id>')
def get_patient_by_id(id):
    patient = db.session.get(Patient, id)
    if not patient:
        return make_response(jsonify({"Error":"Patient not found"}))
    doctor_dict_list = [d.to_dict() for d in patient.doctors]
    patient_dict = (patient.to_dict(rules="-appointments",))
    patient_dict['doctors'] = doctor_dict_list
    return make_response(jsonify(patient_dict), 200)


@app.post('/doctors')
def post_doctors():
    data = request.json
    try: ### try appointments must have at lease one except or a final close ###
        doctor = Doctor(name=data('game'), specialty=data.get('specialty'))
        db.session.add(doctor)
        db.session.commit()
        return make_response(jsonify(doctor.to_dict(rules=("-appointments",))), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"Error": "Doctor MUST have 'Dr.' in their name!"}), 405)
    
@app.post('/appointments')
def post_appointment():
    data = request.json
    try:
        appointment = Appointment(doctor_id = data.get("doctor_id"), patient_id=data.get("patient_id"), day=data.get("day"))
        db.sesson.add(appointment)
        db.session.commmit()
        return make_response(jsonify(appointment.to_dict(rules=("-patient_id", "-doctor_id"))), 201)
    except Exception as e:
        # print(e)
        return make_response(jsonify({"Error": "Invalid appointment: " + str(e)}), 405)

    
@app.patch('/patients/<int:id>') ### needs a for loop and conditional
def patch_patient(id):
    data = request.json
    patient = db.session.get(Patient, id)
    # patient = Patient.query.filter(Patient.id == id).first()
    if not patient:
        return make_response(jsonify({"Error": "Patient not found"}))
    try:
        for key in data:
            setattr(patient, key, data[key])
        db.session.add(patient)
        db.session.commit()
        return make_response(jsonify(patient.to_dict(rules=("-appointments",))), 201)
    except Exception as e:
        return make_response(jsonify({"Error": "Patient data could not be updated."}), 405)


@app.delete('/appointments/<int:id>')
def delete_appointment(id):
    appointment = db.session.get(Appointment, id)
    if not appointment:
        return make_response(jsonify({"Error": "Appointment could not be found!"}), 404)
    db.session.delete(appointment)
    db.session.commit()
    return make_response(jsonify({}), 200)



if __name__ == "__main__":
    app.run(port=5555, debug=True)
