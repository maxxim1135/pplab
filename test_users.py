import pytest
from app import app
from models import Base, Session, engine, Users, Order, Audience
import base64


good_user1 = {
    "username": "John",
    "firstname": "John",
    "lastname": "John",
    "email": "john@mail.com",
    "password": "Abcdefgh",
    "phone": "32487032"
}

good_user2 = {
    "username": "user4",
    "firstname": "Ivan",
    "lastname": "Bober",
    "email": "user3@exampl.com",
    "password": "11111111",
    "phone": "0968797674"
}


class TestCreateUser:

    @pytest.fixture
    def succes1(self):

        user = good_user1
        return user

    @pytest.fixture()
    def fail1(self):
        user = good_user1

        return user

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def test_create_user_succes1(self, succes1):
        self.create_tables()

        responce = app.test_client().post('/user', json=succes1)
        assert responce.status_code == 200

    def test_create_user_fail1(self, fail1):

        responce = app.test_client().post('/user', json=fail1)
        assert responce.status_code == 400


class TestUserGet:

    @pytest.fixture()
    def succes1(self):
        user = {
            "email": "john@mail.com",
            "password": "Abcdefgh",
        }

        return user

    @pytest.fixture()
    def fail1(self):
        user = {
            "email": "john@mail.com",
            "password": "Abcfgh",
        }

        return user

    def test_get_succes1(self, succes1):

        jsons = succes1
        us = Session.query(Users).filter_by(email=jsons['email']).first()
        credentials = b"john@mail.com:Abcdefgh"
        valid_credentials = base64.b64encode(credentials).decode("utf-8")
        responce = app.test_client().get(
            f'/user/{us.user_id}',
            headers={"Authorization": "Basic " + valid_credentials}
        )

        assert responce.status_code == 200

    def test_get_fail1(self, fail1):
        jsons = fail1
        us = Session.query(Users).filter_by(email=jsons['email']).first()
        valid_credentials = base64.b64encode(b"jhn@mail.com:Abcdefgh").decode("utf-8")
        responce = app.test_client().get(
            f'/user/{us.user_id}',
            headers={"Authorization": "Basic " + valid_credentials}
        )

        assert responce.status_code == 401

    def test_get_fail2(self, fail1):
        jsons = fail1
        us = Session.query(Users).filter_by(email=jsons['email']).first()
        valid_credentials = base64.b64encode(b"john@mail.com:Abcdefgh").decode("utf-8")
        responce = app.test_client().get(
            f'/user/{111}',
            headers={"Authorization": "Basic " + valid_credentials}
        )

        assert responce.status_code == 404


class TestUserPut:

    @pytest.fixture()
    def succes1(self):
        # user = good_user1
        user_to_update = {
            "password": "1"
        }
        return user_to_update

    @pytest.fixture()
    def fail1(self):
        user = {
            "firstname": "John"
        }

        return user

    def test_user_put_success1(self, succes1):
        session = Session()

        us = session.query(Users).filter_by(email=good_user1['email']).first()
        valid_credentials = base64.b64encode(b"john@mail.com:Abcdefgh").decode("utf-8")
        responce = app.test_client().put(
            f'/user/?user_id={us.user_id}',
            headers={"Authorization": "Basic " + valid_credentials},
            json = succes1
        )
        print(responce.data)
        assert responce.status_code == 200

    def test_400(self, fail1):
        jsons = fail1
        session = Session()
        us = session.query(Users).filter_by(email=good_user1['email']).first()
        valid_credentials = base64.b64encode(b"john@mail.com:1").decode("utf-8")
        responce = app.test_client().put(
            f'/user/?user_id={us.user_id}',
            headers={"Authorization": "Basic " + valid_credentials},
            json=fail1
        )

        assert responce.status_code == 400

    def test_401(self, succes1):
        jsons = succes1
        session = Session()
        us = session.query(Users).filter_by(email=good_user1['email']).first()
        valid_credentials = base64.b64encode(b"jhn@mail.com:john@mail.com").decode("utf-8")
        responce = app.test_client().put(
            f'/user/?user_id={1}',
            headers={"Authorization": "Basic " + valid_credentials},
            json=succes1
        )

        print(responce.data)
        assert responce.status_code == 401


class TestUserDelete:

    @pytest.fixture()
    def succes1(self):
        user = {
            "password": "john@mail.com"
        }

        return user

    def test_200(self, succes1):

        us = Session.query(Users).filter_by(email='john@mail.com').first()
        valid_credentials = base64.b64encode(b"john@mail.com:1").decode("utf-8")

        responce = app.test_client().delete(
            f'/user/{us.user_id}',
            headers={"Authorization": "Basic " + valid_credentials}
        )

        assert responce.status_code == 200

    def test_401(self, succes1):

        us = Session.query(Users).filter_by(email='jon@mail.com').first()
        valid_credentials = base64.b64encode(b"john@mail.com:Abcdefgh").decode("utf-8")

        responce = app.test_client().delete(
            f'/user/{111}',
            headers={"Authorization": "Basic " + valid_credentials}
        )

        assert responce.status_code == 401


