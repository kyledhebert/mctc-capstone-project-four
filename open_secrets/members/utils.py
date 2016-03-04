import requests

from core.utils import get_env_variable

OPEN_SECRETS_API = get_env_variable("OPEN_SECRETS_API")


def get_legislators(state):
    """Returns a legislator list from the OpenSecrets API"""
    payload = {'id': 'state', 'apikey': OPEN_SECRETS_API}
    request = requests.get(
        'http://www.opensecrets.org/api/?method=getLegislators',
        params=payload)
    return request
