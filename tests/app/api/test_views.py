import json

import pytest
from flask import Response

from app.db_function import create_user_test


@pytest.fixture
def get_token(client, app):
    # Populate db
    with app.app_context():
        create_user_test()

    # Get token
    get_token_headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Basic YWR2aWNlaGVhbHRoOmFkdmljZWhlYWx0aA==",
    }
    token: str = (
        client.post("/api/login", headers=get_token_headers).get_json().get("token")
    )

    return token


@pytest.fixture
def headers(get_token) -> dict:
    return {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {get_token}",
    }


def test_health_check(client):
    response: Response = client.get("/health-check")
    assert response.status_code == 200


def test_login(client, app):
    # Create user test
    with app.app_context():
        create_user_test()

    # Send request
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Basic YWR2aWNlaGVhbHRoOmFkdmljZWhlYWx0aA==",
    }
    response: Response = client.post("/api/login", headers=headers)
    assert response.status_code == 200


def test_car(client, headers):
    # Send request
    data: dict = {
        "owner": {"name": "Augusto", "cpf": "68175541016"},
        "cars": [
            {"model": "hatch", "color": "blue"},
            {"model": "sedan", "color": "yellow"},
            {"model": "convertible", "color": "gray"},
        ],
    }
    response: Response = client.post("/api/car", headers=headers, data=json.dumps(data))
    assert response.get_json() == {"message": "success"}
    assert response.status_code == 201


def test_invalid_car_color(client, headers):
    data: dict = {
        "owner": {"name": "Augusto", "cpf": "68175541016"},
        "cars": [
            {"model": "convertible", "color": "orange"},
        ],
    }
    response: Response = client.post("/api/car", headers=headers, data=json.dumps(data))
    assert response.status_code == 400
    assert response.get_json() == {
        "cars": {
            "0": {
                "color": {
                    "error_message": "orange color is invalid, enter a valid color for the car"
                }
            }
        }
    }


def test_invalid_car_model(client, headers):
    data: dict = {
        "owner": {"name": "Augusto", "cpf": "68175541016"},
        "cars": [
            {"model": "other", "color": "blue"},
        ],
    }
    response: Response = client.post("/api/car", headers=headers, data=json.dumps(data))
    assert response.status_code == 400
    assert response.get_json() == {
        "cars": {
            "0": {
                "model": {
                    "error_message": "other model is invalid, enter a valid model for the car"
                }
            }
        }
    }
