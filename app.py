"""
Main file with api methods
"""


from flask import Flask
from flask import jsonify, request
from sqlalchemy import exc
from flask_bcrypt import check_password_hash
from flask_httpauth import HTTPBasicAuth
import util_func
import db_utils
from schemas import *
from models import *

app = Flask(__name__)
auth = HTTPBasicAuth()


session = Session()


@auth.verify_password
def verify_password(email, password):
    try:
        user = Session.query(Users).filter_by(email=email).one()
        if check_password_hash(user.password, password):
            return True
        else:
            return False
    except exc.NoResultFound:
        return False


@auth.get_user_roles
def get_user_roles(email):
    try:
        user_db = Session.query(Users).filter_by(email=email).one()
        if user_db.isAdmin:
            return 'admin'
        else:
            return ''
    except exc.NoResultFound:
        return ''


@app.route("/user", methods=["POST"])
def create_user():
    try:
        user_data = UserRegister().load(request.json)
        user = db_utils.create_entry(Users, **user_data)
        return jsonify(UserInfo().dump(user))
    except ValidationError or exc.IntegrityError:
        return "Validation error", 400


@app.route("/user/<int:user_id>", methods=["GET"])
@auth.login_required()
def get_user(user_id):
    try:
        auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)
        user = db_utils.get_entry_by(Users, user_id, Users.user_id)
        if int(user_id) == int(auth_user.user_id):
            return jsonify(UserInfo().dump(user))
        else:
            return jsonify("Authorization error"), 401
    except exc.NoResultFound:
        return jsonify({"Error404": "User not found"}), 404


@app.route("/user/", methods=["PUT"])
@auth.login_required()
def update_user():
    args = request.args
    user_id = args.get('user_id')
    try:
        user_data = UserToUpdate().load(request.json)
        auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)

        if int(user_id) == auth_user.user_id:
            user = db_utils.get_entry_by(Users, user_id, Users.user_id)
            db_utils.update_entry(user, **user_data)
            return jsonify("User update"), 200
        else:
            return jsonify("Authorization error"), 401

    except exc.NoResultFound:
        return jsonify({"Error404": "User not found"}), 404
    except ValidationError or exc.IntegrityError:
        return jsonify("Validation error"), 400


@app.route("/user/<int:user_id>", methods=["DELETE"])
@auth.login_required()
def delete_user_orders(user_id):
    try:
        auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)

        if user_id == auth_user.user_id:

            user_orders = db_utils.get_entries_by(Order, user_id, Order.id_user)
            for i in user_orders:
                db_utils.delete_entry_by(Order, i.order_id, Order.order_id)
            db_utils.delete_entry_by(Users, user_id, Users.user_id)

            return jsonify("User and user's orders are deleted"), 200
        else:
            return jsonify("Authorization error"), 401
    except exc.NoResultFound:
        return jsonify("Error404: User not found"), 404


###########################################################################


@app.route("/Audience", methods=["POST"])
@auth.login_required()
def create_audience():
    try:
        auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)

        if auth_user.isAdmin:
            audience_data = AddUpdateAudience().load(request.json)
            audience = db_utils.create_entry(Audience, **audience_data)
            return jsonify(InfoAudience().dump(audience))
        else:
            return jsonify("Forbidden method"), 403

    except ValidationError as err:
        return str(err), 400


@app.route("/Audience/<int:audience_id>", methods=["GET"])
@auth.login_required()
def get_audience(audience_id):
    try:
        audience = session.query(Audience).filter_by(audience_id=audience_id).one()
        return jsonify(InfoAudience().dump(audience))
    except exc.NoResultFound:
        return jsonify({"Error404": "Audience not found"}), 404


@app.route("/Audience/", methods=["PUT"])
@auth.login_required()
def update_audience():
    args = request.args
    audience_id = args.get('audience_id')
    auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)

    if auth_user.isAdmin:
        try:
            audience_data = AddUpdateAudience().load(request.json)
            audience = session.query(Audience).filter_by(audience_id=audience_id).one()
            db_utils.update_entry(audience, **audience_data)
            session.commit()
            return jsonify("Audience update"), 200
        except exc.NoResultFound:
            return jsonify({"Error404": "Audience not found"}), 404
        except ValidationError as err:
            return str(err), 400
    else:
        return "Forbidden method", 403


@app.route("/Audience/<int:audience_id>", methods=["DELETE"])
@auth.login_required()
def delete_audience(audience_id):

    auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)

    if auth_user.isAdmin:
        try:
            user_orders = db_utils.get_entries_by(Order, audience_id, Order.id_audience)
            for i in user_orders:
                db_utils.delete_entry_by(Order, i.order_id, Order.order_id)
            db_utils.delete_entry_by(Users, audience_id, Order.id_audience)
            return jsonify("Audience and user's tickets are deleted"), 200
        except exc.NoResultFound:
            return jsonify("Error404: Audience not found"), 404
    else:
        return "Forbidden method", 403


###########################################################################

@app.route("/Order", methods=["POST"])
@auth.login_required()
def create_order():
    try:
        args = request.get_json()
        audience_id = args.get('id_audience')
        end_time = args.get('end_time')
        start_time = args.get('start_time')
        user_id = args.get('id_user')

        auth_user = db_utils.get_entry_by(Users, auth.username(), Users.email)

        if auth_user.user_id == int(user_id):
            if not util_func.check_time(audience_id, end_time, start_time):
                return jsonify("Wrong date"), 400
            add_order_schema = AddOrder()
            order = add_order_schema.load(args, session=session)
            session.add(order)
            session.commit()
            return add_order_schema.dump(order), 200
        else:
            return jsonify("You can create order only for yourself"), 401

    except ValidationError as err:
        return str(err), 400
    except exc.NoResultFound:
        return jsonify({"Error404": "Ids not found"}), 404


@app.route("/Order/<int:order_id>", methods=["GET"])
@auth.login_required()
def get_order(order_id):

    user = db_utils.get_entry_by(Users, auth.username(), Users.email)
    orders = db_utils.get_entries_by(Order, user.user_id, Order.id_user)

    for i in orders:
        if i.order_id == order_id:
            try:
                order = session.query(Order).filter_by(order_id=order_id).one()
                return jsonify(OrderInfo().dump(order))
            except exc.NoResultFound:
                return jsonify({"Error404": "Order not found"}), 404

    return jsonify({"Error404": "Order not found"}), 404


@app.route("/Order/", methods=["PUT"])
@auth.login_required()
def update_order():
    args = request.args
    order_id = args.get('order_id')

    user = db_utils.get_entry_by(Users, auth.username(), Users.email)
    orders = db_utils.get_entries_by(Order, user.user_id, Order.id_user)

    for i in orders:
        if i.order_id == int(order_id):
            try:
                audience_data = UpdateOrder().load(request.json)
                order = session.query(Order).filter_by(order_id=order_id).one()
                db_utils.update_entry(order, **audience_data)
                return jsonify("Order update"), 200
            except ValidationError as err:
                return str(err), 400

    return jsonify({"Error404": "Order not found"}), 404


@app.route("/Order/", methods=["DELETE"])
@auth.login_required()
def delete_order():
    args = request.args
    order_id = args.get('order_id')

    user = db_utils.get_entry_by(Users, auth.username(), Users.email)
    orders = db_utils.get_entries_by(Order, user.user_id, Order.id_user)

    for i in orders:
        if i.order_id == int(order_id):
            db_utils.delete_entry_by(Order, order_id, Order.order_id)
            return "Order deleted", 200

    return jsonify({"Error404": "Order not found"}), 404


if __name__ == '__main__':
    app.run()
