import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.models import User, db

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

    # this is a new test session, we have to register the user again

    response = client.post("/register", data = {
        "email": "marius@yahoo.com",
        "password": "123456",
        "name": "Marius"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/login"

    response = client.post("/login", data = {
        "email": "marius@yahoo.com",
        "password": "123456",
        "submit": "Login"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/"

    response = client.post("/login", data = {
        "email": "gabi@yahoo.com",
        "password": "123456"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/login"

def test_logout(client):

    # this is a new test session, we have to register the user again

    response = client.post("/register", data={
        "email": "marius@yahoo.com",
        "password": "123456",
        "name": "Marius"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/login"

    client.post("/login", data={
        "email": "marius@yahoo.com",
        "password": "123456"
    }, follow_redirects=True)

    response = client.get("/")

    assert response.status_code == 200
    #assert b'href="/logout"' not in response.data
    assert b'href="/logout"' in response.data

    logout_response = client.get("/logout", follow_redirects=True)

    assert logout_response.status_code == 200
    assert b'href="/logout"' not in logout_response.data
    #assert b'href="/logout"' in logout_response.data

