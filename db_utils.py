from models import *


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def get_users(model_class, param, **kwargs):

    session = Session()
    if isinstance(param, int):
        return session.query(model_class).filter_by(event_id=param, **kwargs).all()
    else:
        user = get_entry_by_uid(Users, param)
        return session.query(model_class).filter_by(user_id=user.user_id, **kwargs).all()


def get_entry_by_uid(model_class, user_id, **kwargs):
    session = Session()
    return session.query(model_class).filter_by(user_id=user_id, **kwargs).one()


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    else:
        return entry


def delete_entry_by_uid(model_class, user_id, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(user_id=user_id, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry_by_aid(model_class, audience_id, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(audience_id=audience_id, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry_by_oid(model_class, order_id, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(order_id=order_id, **kwargs).delete()
    if commit:
        session.commit()


def get_orders_by_uid(model_class, param, **kwargs):
    session = Session()
    if isinstance(param, int):
        return session.query(model_class).filter_by(id_user=param, **kwargs).all()
    else:
        user = get_entry_by_uid(Users, param)
        return session.query(model_class).filter_by(id_user=user.id_user, **kwargs).all()


def get_orders_by_aid(model_class, param, **kwargs):
    session = Session()
    if isinstance(param, int):
        return session.query(model_class).filter_by(id_audience=param, **kwargs).all()
    else:
        user = get_entry_by_uid(Users, param)
        return session.query(model_class).filter_by(id_audience=user.audience_id, **kwargs).all()

