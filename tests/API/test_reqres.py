import jsonschema
import requests

from tests.utils import load_schema


def test_get_list_users():
    response = requests.get(
        url='https://reqres.in/api/users',
        params={"page": 2}
    )

    assert response.status_code == 200
    assert response.json()["page"] == 2


def test_get_single_existing_user():
    response = requests.get(url='https://reqres.in/api/users/2')

    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2


def test_get_user_not_found():
    response = requests.get(url='https://reqres.in/api/users/23')

    assert response.status_code == 404


def test_get_user_schema_validation():
    schema = load_schema('get_users.json')

    response = requests.get(url='https://reqres.in/api/users/2')

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_add_new_user():
    response = requests.post(
        url='https://reqres.in/api/users',
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "morpheus"


def test_update_user():
    schema = load_schema('update_user.json')

    response = requests.put(
        url='https://reqres.in/api/users/2',
        json={
            "name": "morpheus",
            "job": "zion resident"
        }
    )

    assert response.json()["job"] == 'zion resident'
    jsonschema.validate(response.json(), schema)


def test_delete_user():
    response = requests.delete(url='https://reqres.in/api/users/2')

    assert response.status_code == 204


def test_successful_registration_schema_validation():
    schema = load_schema('registration_user.json')

    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_successful_login_status_code():
    response = requests.get(
        url='https://reqres.in/api/login',
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
            }
    )

    assert response.status_code == 200


def test_unsuccessful_login():
    response = requests.post(
        url='https://reqres.in/api/login',
        json={
            "email": "peter@klaven"
            }
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
