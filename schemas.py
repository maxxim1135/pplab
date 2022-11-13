from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.security import generate_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_bcrypt import generate_password_hash

from models import *


def validate_email(emeil1):
    if not (session.query(Users).filter(Users.email == emeil1).count() == 0):
        raise ValidationError("Email exists")


class UserInfo(Schema):
    user_id = fields.Integer()
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()


class UserRegister(Schema):
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    email = fields.Email(validate=validate_email)
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )
    phone = fields.String()


class UserToUpdate(Schema):
    email = fields.Email(validate=validate_email)
    password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )


class InfoAudience(Schema):
    audience_id = fields.Integer()
    address = fields.String()
    seats_count = fields.Integer()


class AddUpdateAudience(Schema):
    address = fields.String()
    seats_count = fields.Integer()


class OrderInfo(Schema):
    order_id = fields.Integer()
    start_time = fields.String()
    end_time = fields.String()
    id_user = fields.Integer()
    id_audience = fields.Integer()


session = Session()


def validate_id_user(id_user):
    if session.query(Users).filter_by(user_id=id_user).count() == 0:
        return False
    return True


def validate_id_audience(id_audience):
    if session.query(Audience).filter_by(audience_id=id_audience).count() == 0:
        return False
    return True


def validate_start_time(start_time):
    if not (session.query(Order).filter(Order.start_time == start_time).count() == 0):
        raise ValidationError("Order exists")


def validate_end_time(end_time):
    if not (session.query(Order).filter(Order.end_time == end_time).count() == 0):
        raise ValidationError("Order exists")


class AddOrder(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = False
        include_fk = True
        load_instance = True

    id_user = fields.Integer(validate=validate_id_user)
    id_audience = fields.Integer(validate=validate_id_audience)

    start_time = fields.String()
    end_time = fields.String()


class UpdateOrder(Schema):
    id_user = fields.Integer()
    id_audience = fields.Integer()
