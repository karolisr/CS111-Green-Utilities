# -*- coding: utf-8 -*-
"""http"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import HTTPError

ACC_HEAD = {
    'csv': {'Accept': 'text/csv'},
    'fasta': {'Accept': 'text/x-fasta'},
    'json': {'Accept': 'application/json'},
    'text': {'Accept': 'text/plain'},
    'asn.1': {'Accept': 'text/plain'},
    'xml': {'Accept': 'application/xml'},
}


def _valid_response_formats():
    return tuple(ACC_HEAD.keys())


def retry_session(retries=5, backoff_factor=1,
                  status_forcelist=(500, 502, 504)):  # noqa

    session = requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)

    adapter = HTTPAdapter(max_retries=retry)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


def get(url, params=None, response_format='json'):  # noqa
    if type(response_format) in (dict, ):
        headers = response_format
    else:
        assert response_format in _valid_response_formats()
        headers = ACC_HEAD[response_format]

    with retry_session() as session:
        response = session.get(url=url, params=params, headers=headers)

    try:
        response.raise_for_status()
    except HTTPError as e:
        print(e)

    return response


def post(url, data, response_format):  # noqa
    assert response_format in _valid_response_formats()
    headers = ACC_HEAD[response_format]

    with retry_session() as session:
        response = session.post(url=url, data=data, headers=headers)

    try:
        response.raise_for_status()
    except HTTPError as e:
        print(e)

    return response
