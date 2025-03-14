import requests
from requests import JSONDecodeError


def create_request_header(token):
    return {'Authorization': f'Token {token}'}


def request_data(endpoint, token, payload=None, timeout=None):
    """ Retrieve data from DDM. """
    headers = create_request_header(token)
    r = requests.get(endpoint, headers=headers, params=payload, timeout=timeout)
    r.raise_for_status()

    if r.ok:
        try:
            return r.json()
        except JSONDecodeError:
            return {'errors': ['JSONDecodeError']}
    else:
        return {
            'errors': ['request not okay'],
            'r': r
        }
