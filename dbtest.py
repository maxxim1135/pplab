from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from models import *

engine = create_engine('mssql+pymssql://sa:Pass123!@localhost/pp_var_7')
engine.dialect.identifier_preparer.initial_quote = ''
engine.dialect.identifier_preparer.final_quote = ''
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()

users = [
    user(username="BrianMay123", firstname="Brian", lastname="May", phone="1231231231", email="brianmay@gmail.com", password="oaoa13o132"),
    user(username="JimPage", firstname="Jimmy", lastname="Page", phone="151141241", email="jimmypage@gmail.com", password="straesthedan")
]

Audiences = [
    audience(address="St. Stepana Bandery 16", seats_count=100),
    audience(address="St. Lychakivska 47", seats_count=120)
]

orders = [
    order(start_time="12.01.1999 12:12:12", end_time="12.01.1999 12:12:12", user_id=1, audience_id=2),
    order(start_time="12.01.1999 12:12:12", end_time="12.01.1999 12:12:12", user_id=2, audience_id=1)
]


def create_users():
    for us in users:
        Session.add(us)
    Session.commit()


def create_audiences():
    for aud in Audiences:
        Session.add(aud)
    Session.commit()


def create_ord():
    for o in orders:
        Session.add(o)
    Session.commit()


create_users()