from werkzeug.security import generate_password_hash

from models import *


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


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


def delete_entry(model_class, user_id, *, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter_by(user_id=user_id, **kwargs).delete()
    if commit:
        session.commit()
