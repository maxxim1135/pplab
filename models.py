"""
SQLAlchemy models classes, which describe database tables
and use for migration
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATETIME, BOOLEAN
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session


engine = create_engine('mysql://root:ab?sad132FF..@localhost:3306/7var')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class Users(Base):
    __tablename__ = "user"

    user_id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(45), nullable=False)
    firstname = Column('firstname', String(45), nullable=False)
    lastname = Column('lastname', String(45), nullable=False)
    email = Column('email', String(45), unique=True, nullable=False)
    password = Column('password', String(400), nullable=False)
    phone = Column('phone', String(10), unique=True, nullable=False)
    isAdmin = Column('isAdmin', BOOLEAN, default=False)


class Audience(Base):
    __tablename__ = "Audience"

    audience_id = Column('audience_id', Integer, primary_key=True)
    address = Column('address', String(45), nullable=False)
    seats_count = Column('seats_count', Integer, nullable=False)


class Order(Base):
    __tablename__ = "Order"

    order_id = Column('order_id', Integer, primary_key=True,)
    start_time = Column('start_time', DATETIME, nullable=False)
    end_time = Column('end_time', DATETIME, nullable=False)
    id_user = Column('user_id', ForeignKey(Users.user_id), nullable=False)
    id_audience = Column('audience_id', ForeignKey(Audience.audience_id), nullable=False)
