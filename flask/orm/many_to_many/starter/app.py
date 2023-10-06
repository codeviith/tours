from flask import make_response, jsonify, request, g
from flask import Flask
from models import db, Student, Course, Enrollment

from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def root():
    return "<h1>Registrar</h1>"

@app.get('/students')
def get_students():
    student_list = Student.query.all()
    student_json = []
    for student in student_list:
        student_json.append(student.to_dict(rules=("-enrollment_list", )))
    return make_response(jsonify(student_json), 200)

@app.get('/students/<int:id>')
def get_students_by_id(id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return make_response(jsonify({"error":"no such student!"}), 404)
    return make_response(jsonify(student.to_dict()), 200)

@app.get('/students/<int:id>/courses')
def get_courses_for_students(id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return make_response(jsonify({"error":"no such student!"}), 404)
    # association proxy
    # courses = [course.to_dict(rules=("=enrollment_list", )) for courses in student.courses]
    # manually hopping tables

    courses = [e.course_object.to_dict(rules=("-enrollment_list",)) for e in student.enrollment_list]
    return make_response(jsonify(courses), 200)

@app.post('/students/<int:id>/enrollments')
def post_enrollment(id):
    student = db.session.get(Student, id)
    # student = Student.query.filter(Student.id == id).first()
    if not student:
        return make_response(jsonify({"error":"no such student!"}), 404)
    data = request.json
    enrollment = Enrollment(student_id = student.id, course_id = data['course_id'], term=data["term"])
    # enrollment = Enrollment(student_id = student.id, course_id=data.get("course_id"), term=data.get("term"))

    try: ### This is needed everytime we POST or PATCH
        db.session.add(enrollment)
        db.session.commit()
    except ValueError as e:
        return make_response(jsonify({"error": "Invalid term"}, 404))
    return make_response(jsonify(enrollment.to_dict(rules=("-student_object",))),201)


@app.patch('/students/<int:id>')
def patch_student(id):
    student = db.session.get(Student, id)
    if not student:
        return make_response(jsonify({"error": "No such student"}), 404)
    data = request.json
    
    try:
        '''
        data {
            grad_year:2024
            lname: Wiggins
        }
        '''
        for key in data:
            '''
            key == "grad_year"
            data[key] == 2024
            student.grad_year = 2024
            student.lname = Wiggins
            '''
            setattr(student, key, data[key])
        db.session.add(student)
        db.session.commit()

        return make_response(jsonify(student.to_dict(rules = ("-enrollment_list",)), 201))
    except ValueError as e:
        print(e)
        return make_response(jsonify({"error": "Invalid graduation year"}), 404)
    
@app.delete('/students/<int:id>')
def delete_student(id):
    student = db.session.get(Student, id)
    if not student:
        return make_response(jsonify({"error": "No such student"}), 404)
    db.session.delete(student)
    db.session.commit()
    return make_response(jsonify({}), 200)



if __name__ == "__main__":
    app.run(port=5555, debug=True)

