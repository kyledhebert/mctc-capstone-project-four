import requests

from core.utils import get_env_variable

from .models import Legislator, Organization

OPEN_SECRETS_API = get_env_variable("OPEN_SECRETS_API")


def verify_api_response(request):
    """Checks for HTTPError from API calls"""
    # make sure we get a 200 response
    try:
        request.raise_for_status()
    except  requests.exceptions.HTTPError as e:
        # this will catch anything that isn't a 2XX (4XX, 5XX)
        return "Error: {}".format(e)

    return request    


def verify_JSON_object(request):
    """Verifies repsonse contains a JSON object"""
    # make sure we get a JSON object
    try:
        request.json()
    except ValueError as e:
        return "Error: {}".format(e)

    return request    


def get_legislator_list(state):
    """Returns a list of legislators"""
    # pass the state to get a JSON response from the API
    response = get_legislators(state)
    # parse that response into our list
    legislator_list = parse_legislators(response)
    return legislator_list


def get_legislators(state):
    """Returns a legislator JSON response from the OpenSecrets API"""
    payload = {'id': state, 'apikey': OPEN_SECRETS_API}
    request = requests.get(
        'http://www.opensecrets.org/api/?method=getLegislators&output=json',
        params=payload)

    # exception handling
    verify_api_response(request)
    verify_JSON_object(request)

    return request.json()


def parse_legislators(response):
    """Returns a list of Legislator objects"""
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


def get_contributors_list(candidate_id):
    """Returns a list of contributors from the JSON response"""
    # pass the candidate id to get a JSON response from the API
    response = get_contributors(candidate_id)
    # parse the response to get the list of contributors
    contributors_list = parse_contributors(response)
    return contributors_list


def get_contributors(candidate_id):
    """Returns a JSON response from the Open Secrets API"""
    payload = {'cid': candidate_id, 'apikey': OPEN_SECRETS_API, 'cycle': 2016}
    request = requests.get(
        'http://www.opensecrets.org/api/?method=candContrib&output=json',
        params=payload)

    # exception handling
    verify_api_response(request)
    verify_JSON_object(request)

    return request.json()


def parse_contributors(response):
    """Returns a list of Legislator objects"""
    # create a list for storing Organization objects
    contributor_list = []
    # unpack the JSON response
    response_dict = response.get('response')
    contributors_dict = response_dict.get('contributors')
    json_contributor_list = contributors_dict.get('contributor')
    for contributor in range(len(json_contributor_list)):
        contributor_dict = json_contributor_list[contributor]
        attributes_dict = contributor_dict.get('@attributes')
        # now we have a dict of individual contributor values
        # create a organization instance and assign the values
        organization = create_organization(attributes_dict)
        # add the organization to the list
        contributor_list.append(organization)
    # return the list
    return contributor_list


def create_organization(attributes_dict):
    """Returns an Organization object with its values assigned"""
    # create a new organization instance and assign its values from the dict
    organization = Organization(
        name = attributes_dict.get('org_name'),
        total_contributed = attributes_dict.get('total'),
        pac_contributions = attributes_dict.get('pacs'),
        individual_contributions = attributes_dict.get('indivs')
        )
    return organization
    