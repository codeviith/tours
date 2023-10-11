#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Client, Server, Message  # import your models here!

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)



@app.get("/")
def index():
    return "client/server"



@app.get("/clients")
def get_clients():
    '''
    for each client:
        convert client to dict
        get all servers for client (convert to dict)
        add server dict list to client json
        add final result to list
    '''
    # Query the database following our request to get all our data
    clients = Client.query.all()
    print(clients) # [<Client123434>, <Client448920384>, ...]

    # Structure the data into relevant JSON to return to frontend
    # A.K.A. Convert Pythonic data into JavaScript-readable data
    client_json_list = []
    for client in clients:
        # print(client.name)
        client_dict = client.to_dict()

        server_dict_list = []
        for server in client.servers:
            server_dict_list.append(server.to_dict())
        # server_dict_list = [server.to_dict() for server in client.servers]
        
        client_dict["servers"] = server_dict_list
        client_json_list.append(client_dict)
        # {'kash': [{'jacket': ..., 'hat': ...}],
        #  'chett': [{'coat'}],
        #  'daniel': [{}]}
    return make_response(jsonify(client_json_list), 200)



@app.post('/servers')
def post_server():
    data = request.json

    try:
        server = Server(name=data.get('name'))
        db.session.add(server)
        db.session.commit()
        return make_response(jsonify(server.to_dict(rules="-messages")), 201)
    except:
        return make_response(jsonify({"Error": "Could not creater server!"}), 405)
        


@app.post('/messages')
def post_message():
    data = request.get_json()

    try:
        client = db.session.get(Client.data.get("client_id"))
        if not client:
            return make_response(jsonify({"Error": "No such client"}), 404)
        server = db.session.get(Server.data.get("server_id"))
        if not server:
            return make_response(jsonify({"Error": "No such Server"}), 404)
        msg = Message(
            client=client,
            server=server,
            content=data.get("content"),
        )
        db.session.add(msg)
        db.session.commit()
        return make_response(jsonify(msg.to_dict(rules=("-client_id", "-server_id"))))
    except Exception as e:
        print(e)
        return make_response(jsonify({"Error": "Could not send message."}), 405)



@app.patch('/messages/<int:id>')
def patch_message(id):
    data = request.json
    msg = db.session.get(Message, id)
    if not msg:
        return make_response(jsonify({"Error": "no such message"}), 404)
    try:
        for key in data:
            setattr(msg, key, data[key])
        db.session.add(msg)
        db.session.commit()
        return make_response(jsonify(msg.to_dict()))
    except:
        return make_response(jsonify({"Error": "No such message"}), 405)



@app.delete('/messages/<int:id>')
def delete_msg(id):
    msg = db.session.get(Message, id)
    if not msg:
        return make_response(jsonify({"Error": "no such message"}), 404)
    db.session.delete(msg)
    db.session.commit()
    return make_response(jsonify({}), 200)



if __name__ == "__main__":
    app.run(port=5555, debug=True)
