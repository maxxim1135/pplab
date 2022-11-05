from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine('mssql+pymssql://sa:Pass123!@localhost/pp_var_7')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class user(Base):
    __tablename__ = "user"

    user_id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(45))
    firstname = Column('firstname', String(45))
    lastname = Column('lastname', String(45))
    email = Column('email', String(255))
    password = Column('password', String(45))
    phone = Column('phone', String(10))


class audience(Base):
    __tablename__ = "audience"

    audience_id = Column('audience_id', Integer, primary_key=True)
    address = Column('address', String(45))
    seats_count = Column('datatime', String(45))


class order(Base):
    __tablename__ = "order"

    order_id = Column('order_id', Integer, primary_key=True)
    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime)
    user_id = Column('user_id', ForeignKey(user.user_id))
    audience_id = Column('audience_id', ForeignKey(audience.audience_id))
