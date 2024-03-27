import json
import logging

import allure
import requests
from allure_commons._allure import step
from curlify import to_curl


def post_reqres(url, **kwargs):
    with step(f"POST {url}"):
        response = requests.post(url=url, **kwargs)
        curl = to_curl(response.request)
        logging.debug(to_curl(response.request))
        logging.info(f'status code: {response.status_code}')
        allure.attach(body=curl, name="curl", attachment_type=allure.attachment_type.TEXT, extension='txt')
        allure.attach(body=json.dumps(response.json(), indent=4), name="response",
                      attachment_type=allure.attachment_type.JSON, extension='json')
        return response


def get_reqres(url, **kwargs):
    with step(f"GET {url}"):
        response = requests.get(url=url, **kwargs)
        curl = to_curl(response.request)
        logging.info(to_curl(response.request))
        logging.info(f'status code: {response.status_code}')
        allure.attach(body=curl, name="curl", attachment_type=allure.attachment_type.TEXT, extension='txt')
        allure.attach(body=json.dumps(response.json(), indent=4), name="response",
                      attachment_type=allure.attachment_type.JSON, extension='json')
        return response
