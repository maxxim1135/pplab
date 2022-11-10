from flask import Flask
from flask import jsonify, request
from marshmallow import exceptions
from sqlalchemy import exc
from flask import Response

import db_utils
from schemas import *
from models import *

app = Flask(__name__)

session = Session()


@app.route("/user", methods=["POST"])
def create_user():
    try:
        user_data = UserRegister().load(request.json)
        user = db_utils.create_entry(Users, **user_data)
        return jsonify(UserInfo().dump(user))
    except ValidationError as err:
        return str(err), 400


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        # if session.query(Users).filter_by(user_id=user_id).count() == 0:
        #    return "User not found", 404
        user = db_utils.get_entry_by_uid(Users, user_id)
        return jsonify(UserInfo().dump(user))
    except exc.NoResultFound:
        return jsonify({"Error404": "User not found"}), 404


@app.route("/user/", methods=["PUT"])
def update_user():
    args = request.args
    user_id = args.get('user_id')
    try:
        user_data = UserToUpdate().load(request.json)
        user = db_utils.get_entry_by_uid(Users, user_id)
        db_utils.update_entry(user, **user_data)
        return "User update", 200
    except exc.NoResultFound:
        return jsonify({"Error404": "User not found"}), 404
    except ValidationError as err:
        return str(err), 400


@app.route("/user/", methods=["DELETE"])
def delete_user():
    args = request.args
    user_id = args.get('user_id')
    if session.query(Users).filter_by(user_id=user_id).count() == 0:
        return jsonify({"Error404": "User not found"}), 404
    session.query(Users).filter_by(user_id=user_id).delete()
    session.commit()
    return "User deleted", 200


###########################################################################


@app.route("/Audience", methods=["POST"])
def create_audience():
    try:
        audience_data = AddUpdateAudience().load(request.json)
        audience = db_utils.create_entry(Audience, **audience_data)
        return jsonify(InfoAudience().dump(audience))
    except ValidationError as err:
        return str(err), 400


@app.route("/Audience/<int:audience_id>", methods=["GET"])
def get_audience(audience_id):
    try:
        audience = session.query(Audience).filter_by(audience_id=audience_id).one()
        return jsonify(InfoAudience().dump(audience))
    except exc.NoResultFound:
        return jsonify({"Error404": "Audience not found"}), 404


@app.route("/Audience/", methods=["PUT"])
def update_audience():
    args = request.args
    audience_id = args.get('audience_id')
    try:
        audience_data = AddUpdateAudience().load(request.json)
        audience = session.query(Audience).filter_by(audience_id=audience_id).one()
        db_utils.update_entry(audience, **audience_data)
        return "Audience update", 200
    except exc.NoResultFound:
        return jsonify({"Error404": "Audience not found"}), 404
    except ValidationError as err:
        return str(err), 400


@app.route("/Audience/", methods=["DELETE"])
def delete_audience():
    args = request.args
    audience_id = args.get('audience_id')
    if session.query(Audience).filter_by(audience_id=audience_id).count() == 0:
        return "Audience not found", 404
    session.query(Audience).filter_by(audience_id=audience_id).delete()
    session.commit()
    return "Audience deleted", 200


###########################################################################

@app.route("/Order", methods=["POST"])
def create_order():
    try:
        args = request.get_json()
        AddOrder_schema = AddOrder()
        order = AddOrder_schema.load(args, session=session)
        session.add(order)
        session.commit()
        return AddOrder_schema.dump(order)
    except ValidationError as err:
        return str(err), 400


@app.route("/Order/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = session.query(Order).filter_by(order_id=order_id).one()
        return jsonify(OrderInfo().dump(order))
    except exc.NoResultFound:
        return jsonify({"Error404": "Order not found"}), 404


@app.route("/Order/", methods=["PUT"])
def update_order():
    args = request.args
    order_id = args.get('order_id')
    try:
        audience_data = UpdateOrder().load(request.json)
        order = session.query(Order).filter_by(order_id=order_id).one()
        db_utils.update_entry(order, **audience_data)
        return "Order update", 200
    except exc.NoResultFound:
        return jsonify({"Error404": "Order not found"}), 404
    except ValidationError as err:
        return str(err), 400


@app.route("/Order/", methods=["DELETE"])
def delete_order():
    args = request.args
    order_id = args.get('order_id')
    if session.query(Order).filter_by(order_id=order_id).count() == 0:
        return "Order not found", 404
    session.query(Order).filter_by(order_id=order_id).delete()
    session.commit()
    return "Order deleted", 200


if __name__ == '__main__':
    app.run()
