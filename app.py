from flask import Flask
from flask import jsonify, request
from sqlalchemy import exc

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


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_orders(user_id):
    try:
        user_orders = db_utils.get_orders_by_uid(Order, user_id)
        for i in user_orders:
            db_utils.delete_entry_by_oid(Order, i.order_id)
        db_utils.delete_entry_by_uid(Users, user_id)
        return "User and user's tickets are deleted", 200
    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404


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
        session.commit()
        return "Audience update", 200
    except exc.NoResultFound:
        return jsonify({"Error404": "Audience not found"}), 404
    except ValidationError as err:
        return str(err), 400


@app.route("/Audience/<int:audience_id>", methods=["DELETE"])
def delete_audience_orders(audience_id):
    try:
        user_orders = db_utils.get_orders_by_aid(Order, audience_id)
        for i in user_orders:
            db_utils.delete_entry_by_oid(Order, i.order_id)
        db_utils.delete_entry_by_aid(Users, audience_id)
        return "Audience and user's tickets are deleted", 200
    except exc.NoResultFound:
        return jsonify("Error404: Audience not found"), 404


###########################################################################

@app.route("/Order", methods=["POST"])
def create_order():
    try:
        args = request.get_json()
        audience_id = args.get('id_audience')
        end_time = args.get('end_time')
        start_time = args.get('start_time')
        if session.query(Order).filter(Order.id_audience == audience_id).count() > 0:
            if not session.query(Order).filter(Order.id_audience == audience_id). \
                           filter(start_time >= Order.start_time, end_time <= Order.end_time).count() == 0:
                raise ValidationError("Order1 exists")
            elif not session.query(Order).filter(Order.id_audience == audience_id). \
                    filter(start_time < Order.start_time, end_time >= Order.start_time).count() == 0:
                raise ValidationError("Order2 exists")
            elif not session.query(Order).filter(Order.id_audience == audience_id). \
                    filter(start_time <= Order.end_time, end_time > Order.end_time).count() == 0:
                raise ValidationError("Order3 exists")
            elif not session.query(Order).filter(Order.id_audience == audience_id). \
                    filter(start_time <= "2022-11-13").count() == 0:
                raise ValidationError("We live in the present and not in the past")

        AddOrder_schema = AddOrder()
        order = AddOrder_schema.load(args, session=session)
        session.add(order)
        session.commit()
        return AddOrder_schema.dump(order)
    except ValidationError as err:
        return str(err), 400
    except exc.NoResultFound:
        return jsonify({"Error404": "Order not found"}), 404


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
