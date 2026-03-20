import sys
import os
from datetime import date
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.models import BlogPost, db, User

def perform_register(client):

    # CREATE POST REQUEST FIRST
    return client.post("/register", data = {
        "email": "andrei@yahoo.com",
        "password": "123456",
        "name": "andrei"
    }, follow_redirects=True)

def perform_login(client):

    perform_register(client)

    return client.post("/login", data = {
        "email": "andrei@yahoo.com",
        "password": "123456",
    }, follow_redirects=True)

def test_get_all_posts(client):

    response = client.get('/')
    assert response.status_code == 200

def test_add_new_post(client):

    perform_login(client)

    payload = {
        'title': 'Test title',
        'subtitle': 'Test subtitle',
        'body': 'Test body',
        'img_url': 'https://example.com/image.jpg'
    }

    response = client.post('/new-post', data = payload, follow_redirects = True)

    assert response.status_code == 200
    assert payload['title'].encode() in response.data

    new_post = db.session.execute(db.select(BlogPost).where(BlogPost.title == payload['title'])).scalar()

    assert new_post is not None
    assert new_post.title == payload['title']
    assert new_post.subtitle == payload['subtitle']
    assert new_post.body == payload['body']
    assert new_post.img_url == payload['img_url']



