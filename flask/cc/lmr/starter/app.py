#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Right, Left, Middle  # import your models here!

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)



@app.get("/")
def index():
    return "right/left"


@app.get('/rights')
def get_rights():
    rights = Right.query.all()
    data = [right.to_dict(rules=("-middle_list",)) for right in rights]

    return make_response(jsonify(data), 200)


@app.get('/rights/<int:id>')
def get_rights_by_id(id):
    right = Right.query.filter(Right.id == id).first()
    ### rights = db.session.get(Right, id)
    if not right: # So is rights a boolean??
        return make_response(jsonify({"Error":"No such data for Right."}), 404)
    return make_response(jsonify(right.to_dict()), 200)


@app.post('/lefts')
def post_lefts():
    data = request.json

    try:
        left = Left(column=data.get('column'))
        db.session.add(left)
        db.session.commit()
        return make_response(jsonify(left.to_dict(), 200))
    except Exception as e:
        print(e)
        return make_response(jsonify({"Error": "Invalid data: Can't post Left"}), 405)


@app.patch('/middles/<int:id>')
def patch_middles_by_id(id):
    data = request.json

    middle_to_patch = db.session.get(Middle, id)
    if not middle_to_patch:
        return make_response(jsonify({"Error": "No such data for Middle."}), 404)
    
    try:
        for key in data:
            setattr(middle_to_patch, key, data[key])
            db.session.add(middle_to_patch)
            db.session.commit()
            return make_response(jsonify(middle_to_patch.to_dict(rules=("-left", "-right"))), 201)
    except Exception as e:
        print(e)
        return make_response(set({"Error": "Cannot patch Middle."}), 405)


@app.delete('/lefts/<int:id>')
def delete_left_by_id(id):
    left = db.session.get(Left, id)

    if not left:
        return make_response(jsonify({"Error": "No such data for Left."}), 404)
    db.session.delete(left)
    db.session.commit()
    return make_response(jsonify({}), 200)




if __name__ == "__main__":
    app.run(port=5555, debug=True)
