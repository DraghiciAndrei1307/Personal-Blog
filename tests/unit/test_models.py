from project.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def test_new_user():
    '''
    GIVEN a user model
    WHEN a new User is created
    THEN check the email, hashed_password and name are defined correctly
    '''

    user = User(
        email = "andrei@yahoo.com",
        password = generate_password_hash("123456", method='pbkdf2:sha256', salt_length=8),
        name = "Andrei"
    )

    assert user.email == "andrei@yahoo.com"
    assert user.password != "123456"
    assert user.check_password("123456") == user.password
    assert user.name == "Andrei"