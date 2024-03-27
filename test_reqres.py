import json
import logging

import allure
import requests
from allure_commons._allure import step
from jsonschema import validate
from curlify import to_curl
from schemas import GetUsers
from utils import post_reqres, get_reqres

DOMAIN_URL = "https://reqres.in"

USERS_API = "/api/users"


def test_get_users():
    url = "https://reqres.in/api/users"

    response = requests.get(url=url, params={"page": 2})

    assert response.status_code == 200
    assert response.json()['page'] == 2


def test_post_users():
    name = 'abc'
    job = 'fdr'
    payload = {
        "name": name,
        "job": job
    }

    response = post_reqres(DOMAIN_URL + USERS_API, json=payload)
    assert response.status_code == 201
    assert response.json()['name'] == name


def test_schema_validation():
    url = "https://reqres.in/api/users"

    response = get_reqres(url=url, params={"page": 2})

    validate(response.json(), GetUsers)


def test_schema_validation_from_file():
    url = "https://reqres.in/api/users"

    response = requests.get(url=url, params={"page": 2})

    schema = json.load(open('get_users.json'))
    validate(response.json(), schema)
