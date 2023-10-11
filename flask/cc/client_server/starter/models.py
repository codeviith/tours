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


class Server(db.Model, SerializerMixin):
    __tablename__ = "server_table"

    serialize_rules = ("-message_list.servers_obj",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    message_list = db.relationship("Message", back_populates="servers_obj")

    clients = association_proxy("message_list", "clients_obj")

    @validates("name")
    def validate_name(self, key, name):
        if not (name.isupper() and name.isalpha()):
            raise ValueError("Server name must all be capitalized!")
        else:
            return name






class Message(db.Model, SerializerMixin):
    __tablename__ = "message_table"

    serialize_rules = ("-servers_obj.message_list", "-clients_obj.message_list")

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("server_table.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client_table.id"), nullable=False)

    servers_obj = db.relationship("Server", back_populates="message_list")
    clients_obj = db.relationship("Client", back_populates="message_list")

    @validates("content")
    def validate_name(self, key, content):
        if len(string(content)):
            raise ValueError("Content must not be empty")
        return content






class Client(db.Model, SerializerMixin):
    __tablename__ = "client_table"

    serialize_rules = ("-message_list.clients_obj",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    message_list = db.relationship("Message", back_populates="clients_obj" )

    servers = association_proxy("message_list", "servers_obj")

    @validates("name")
    def validate_name(self, key, name):
        if not (len(name) >= 5 and len(name) <= 15):
            raise ValueError("Client name must be between 5 and 15 characters, inclusive!")
        else:
            return name




