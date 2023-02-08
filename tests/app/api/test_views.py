import json

from flask import Response


def test_health_check(client):
    response: Response = client.get("/health-check")
    assert response.status_code == 200


def test_car(client):
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
    }
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
    assert response.status_code == 200


def test_car_invalid_color(client):
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
    }
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
