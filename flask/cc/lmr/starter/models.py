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


class Left(db.Model, SerializerMixin):
    __tablename__ = "left_table"

    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String, nullable=False, unique=True)

    middle_list = db.relationship("Middle", back_populates="left_obj", cascade="all, delete")

    serialize_rules = ("-middle_list.left_obj",)

    rights = association_proxy("middle_list", "right_obj")  ### always has to be 'list', 'object'

    @validates("column")
    def validate_left_column(self, key, column):
        if not isinstance(column, string):
            raise ValueError("Entry must be a string!")
        else:
            return column



class Middle(db.Model, SerializerMixin):
    __tablename__ = "middle_table"

    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String, nullable=False)
    left_id = db.Column(db.Integer, db.ForeignKey('left_table.id'), nullable=False) ### attributes with '=' must be placed at the end!!!!
    right_id = db.Column(db.Integer, db.ForeignKey('right_table.id'),nullable=False)

    left_obj = db.relationship("Left", back_populates="middle_list")
    right_obj = db.relationship("Right", back_populates="middle_list")

    serialize_rules = ("-left_obj.middle_list", "-right_obj.middle_list")

    @validates("column")
    def validate_left_column(self, key, column):
        ### Method 1:
        for char in column:
            if not char in string.punctuation: ### shouldn't this be 'if char not in string.punctuation'??
                raise ValueError("Entry must be a punctuation!")
        return column
        
        ### Method 2:
        # if len(set(column) - set(string.punctuation)) > 0:
        #     raise ValueError("Entry must be a punctuation!")
        # else:
        #     return column
        
        ### Method 3:




class Right(db.Model, SerializerMixin):
    __tablename__ = "right_table"

    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.Integer, nullable=False)

    middle_list = db.relationship("Middle", back_populates="right_obj", cascade="all, delete")

    serialize_rules = ("-middle_list.right_obj",)

    lefts = association_proxy("middle_list", "left_obj")  ### always has to be ('list', 'object')

    @validates("column")
    def validate_left_column(self, key, column):
        if not isinstance(column, int):
            raise ValueError("Entry must be numerical values!")
        else:
            return column
