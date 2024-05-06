import pytest
from app.tests.database import client


# @pytest.fixture
# def test_user():
#     response = client.post(
#         "/accounts/register",
#         json={"username": "eduardo", "password": "you-will-never-guess"},
#     )
#     assert response.status_code == 200
#     return


def test_register(client):
    print("Hola")
    response = client.post(
        "/accounts/register",
        json={"username": "nestor", "password": "you-will-never-guess"},
    )
    assert response.json() == {"message": "User created successfully"}


# def test_login():
#     response = client.post(
#         "/accounts/login",
#         data={"username": "eduardo", "password": "you-will-never-guess"},
#     )
#     assert response.status_code == 200
