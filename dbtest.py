from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from models import *

session = Session

user1 = Users(user_id=1, username="BrianMay123", firstname="Brian", lastname="May", email="brianmay@gmail.com",
             password="oaoa13o132", phone="1231231231")
user2 = Users(user_id=2, username="JimPage", firstname="Jimmy", lastname="Page", email="jimmypage@gmail.com",
             password="straesthedan", phone="151141241")

session.add(user1)
session.add(user2)
session.commit()

audience1 = audience(audience_id=1, address="St. Stepana Bandery 16", seats_count="100")
audience2 = audience(audience_id=2, address="St. Lychakivska 47", seats_count="120")

session.add(audience1)
session.add(audience2)
session.commit()

order1 = order(order_id=1, start_time="2022-01-05 15:30:00", end_time="2022-02-05 15:30:00", id_user=1, id_audience=2)
order2 = order(order_id=2, start_time="2022-02-05 15:30:00", end_time="2022-03-05 15:30:00", id_user=2, id_audience=1)

session.add(order1)
session.add(order2)

session.commit()
