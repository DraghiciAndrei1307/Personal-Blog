import pytest

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

    with flask_app.app_context():
        db.drop_all() # clean everything after the test

# Before we start testing routes, we need to create a user

# TEST register

# def test_register_get(client):
#     response = client.get("/register")
#     assert response.status_code == 200

def test_register_post(client):

    # CREATE POST REQUEST FIRST
    response = client.post("/register", data = {
        "email": "andrei@yahoo.com",
        "password": "123456",
        "name": "andrei"
    }, follow_redirects=True)
    assert response.status_code == 200

    # CHECK THE DATABASE AFTER

    user = db.session.execute(db.select(User).where(User.email == "andrei@yahoo.com")).scalar()
    assert user is not None
    assert user.name == "andrei"

    user = db.session.execute(db.select(User).where(User.email == "gabi@yahoo.com")).scalar()
    assert user is None

def test_login(client):

    response = client.post("/register", data = {
        "email": "marius@yahoo.com",
        "password": "123456",
        "name": "Marius"
    }, follow_redirects=True)
    assert response.status_code == 200

    print(response.headers["Location"])

    response = client.post("/login", data = {
        "email": "marius@yahoo.com",
        "password": "123456",
        "submit": "Login"
    }, follow_redirects=True)

    assert response.headers["Location"] == "/"

    response = client.post("/login", data = {
        "email": "gabi@yahoo.com",
        "password": "123456"
    }, follow_redirects=False)

    assert response.headers["Location"] == "/login"


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
