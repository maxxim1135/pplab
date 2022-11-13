from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session


engine = create_engine('mysql://root:759486@localhost/pp')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class Users(Base):
    __tablename__ = "user"

    user_id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(45))
    firstname = Column('firstname', String(45))
    lastname = Column('lastname', String(45))
    email = Column('email', String(45))
    password = Column('password', String(400))
    phone = Column('phone', String(10))


class Audience(Base):
    __tablename__ = "Audience"

    audience_id = Column('audience_id', Integer, primary_key=True)
    address = Column('address', String(45))
    seats_count = Column('seats_count', Integer)


class Order(Base):
    __tablename__ = "Order"

    order_id = Column('order_id', Integer, primary_key=True,)
    start_time = Column('start_time', DATETIME)
    end_time = Column('end_time', DATETIME)
    id_user = Column('user_id', ForeignKey(Users.user_id))
    id_audience = Column('audience_id', ForeignKey(Audience.audience_id))
