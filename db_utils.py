from models import *


def create_entry(model_class, *, commit=True, **kwargs):
    session = Session()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def update_entry(entry, *, commit=True, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    else:
        return entry


def delete_entry_by(model_class, param, field, commit=True, **kwargs):
    session = Session()
    session.query(model_class).filter(field == param, **kwargs).delete()
    if commit:
        session.commit()


def get_entry_by(model_class, param, field, **kwargs):
    session = Session()
    return session.query(model_class).filter(field == param, **kwargs).one()


def get_entries_by(model_class, param, field, **kwargs):
    session = Session()
    return session.query(model_class).filter(field == param, **kwargs).all()

