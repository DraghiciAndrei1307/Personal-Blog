import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.main import app as flask_app
from project.models import db, User
# WHAT WE ARE TESTING HERE:

# routes that does not exist
# invalid input
# DB down
# empty form
# unauthorized user



@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "your_secret_key"
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["WTF_CSRF_ENABLED"] = False
    with flask_app.app_context():
        db.create_all()

        with flask_app.test_client() as client:
            yield client

        # Perform some cleaning after the test is finished
        db.session.remove()
        db.drop_all()

# Before we start testing routes, we need to create a user

# TEST register

# def test_register_get(client):
#     response = client.get("/register")
#     assert response.status_code == 200



# def test_login_get(client):
#     response = client.get("/login")
#     assert response.status_code == 200
#
# def test_login_post(client):
#     response = client.post("/login", data={"email": "andrei@yahoo.com", "password": "12345"})
#     assert response.status_code == 200

# @pytest.fixture
# def routes():
#     return [
#         '/register',
#         '/login',
#         '/logout',
#         '/',
#         '/post/1',
#         '/post/100',
#         '/post/9999',
#         '/new-post',
#         '/edit-post/1',
#         '/edit-post/100',
#         '/edit-post/9999',
#         'delete/post/1',
#         'delete/post/100',
#         'delete/post/9999',
#     ]
#
# def test_page_exists(client, routes):
#
#     for route in routes:
#         response = client.get(route)
#         assert response.status_code == 200
#
#
# def test_404_page(client):
#     response = client.get("/post/9999")
#     assert response.status_code == 404
#
#
#
# def test_create_post(client):
#     response = client.post("/post", data={"title": "test"})
