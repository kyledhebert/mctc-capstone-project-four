import requests

from core.utils import get_env_variable

from .models import Legislator

OPEN_SECRETS_API = get_env_variable("OPEN_SECRETS_API")


def get_legislator_list(state):
    """Returns a list of legislators"""
    # pass the state to get a JSON response from the API
    response = get_legislators(state)
    # parse that response into our list
    legislator_list = parse_json(response)
    return legislator_list


def get_legislators(state):
    """Returns a legislator JSON response from the OpenSecrets API"""
    payload = {'id': state, 'apikey': OPEN_SECRETS_API}
    request = requests.get(
        'http://www.opensecrets.org/api/?method=getLegislators&output=json',
        params=payload)
    
    # make sure we get a 200 response
    try:
        request.raise_for_status()
    except  requests.exceptions.HTTPerror as e:
        # this will catch anything that isn't a 2XX (4XX, 5XX)
        return "Error: {}".format(e)
    
    # make sure we get a JSON object
    # NOTE: We could get a JSON object that contains the error message
    # instead of the desired API response
    try:
        request.json()
    except ValueError as e:
        return "Error: {}".format(e)

    return request.json()


def parse_json(response):
    """Returns a list of Legislator objects from the JSON repsonse"""
    # create a list for storing Legislator objects
    legislator_list = []
    # unpack the JSON response
    response_dict = response.get('response')
    json_legislator_list = response_dict.get('legislator')
    for legislator in range(len(json_legislator_list)):
        legislator_dict = json_legislator_list[legislator]
        attributes_dict = legislator_dict.get('@attributes')
        # now we have a dict of individual member values
        # create a legislator instance and assign the values
        legislator = create_legislator(attributes_dict)
        # add the legislator to the list
        legislator_list.append(legislator)
    # return the list
    return legislator_list


def create_legislator(attributes_dict):
    """Returns a Legislator instance with its values assigned"""
    # create a new legislator instance and assign the values from the dict
    legislator = Legislator(
        candidate_id=attributes_dict.get('cid'),
        name=attributes_dict.get('firstlast'),
        party=attributes_dict.get('party'),
        votesmart_id=attributes_dict.get('votesmart_id')
        )
    return legislator
