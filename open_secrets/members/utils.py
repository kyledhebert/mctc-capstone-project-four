import requests

from core.utils import get_env_variable

from requests_futures.sessions import FuturesSession

from .models import Legislator, Organization, Rating, NPRStory

# retrieve the API keys from environment variables
OPEN_SECRETS_API = get_env_variable('OPEN_SECRETS_API')
VOTE_SMART_API = get_env_variable('VOTE_SMART_API')
NPR_API = get_env_variable('NPR_API')


def verify_api_response(request):
    """Checks for HTTPError from API calls"""
    # make sure we get a 200 response
    try:
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
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


# API calls to OpenSecrets for generating legislator lists by state
# used by index.html
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


# API calls to OpenSecrets, VoteSmart and NPR to get details for display
# in member_detail.html
def get_details_dict(candidate_name, candidate_id, votesmart_id):
    """Returns a dictionary of contributors and ratings"""
    # start a FuturesSessions so we can make API calls asynchronously
    session = FuturesSession()
    contributors_list = get_contributors_list(session, candidate_id)
    # if there is no votesmart id, pass a string
    if votesmart_id:
        ratings_list = get_ratings_list(session, votesmart_id)
    else:
        ratings_list = ['There are no VoteSmart rankings for this candidate']

    npr_story_list = get_story_list(session, candidate_name)
    details_dict = {'contributors': contributors_list, 'ratings': ratings_list,
                    'stories': npr_story_list}
    return details_dict


def get_story_list(session, candidate_name):
    """Return a list of NPR headlines and urls"""
    # pass the candidate_name to get a JSON response from the NPR API
    response = get_stories(session, candidate_name)
    # parse the response to get a list of stories
    story_list = parse_stories(response)
    return story_list


def get_ratings_list(session, votesmart_id):
    """Returns a list of member ratings"""
    # pass the votesmart id to get a JSON response from the API
    response = get_ratings(session, votesmart_id)
    # parse the response to get a list of ratings
    ratings_list = parse_ratings(response)
    return ratings_list


def get_contributors_list(session, candidate_id):
    """Returns a list of contributors from the JSON response"""
    # pass the candidate id to get a JSON response from the API
    response = get_contributors(session, candidate_id)
    # parse the response to get the list of contributors
    contributors_list = parse_contributors(response)
    return contributors_list


def get_stories(session, candidate_name):
    """Returns a JSON response from the NPR API"""
    payload = {'apiKey': NPR_API, 'searchTerm': candidate_name}
    request = session.get(
        'http://api.npr.org/query?fields=title&output=JSON'
        '&searchType=mainText', params=payload)

    # make sure we get a vaiid HTTP response and a JSON object
    verify_api_response(request.result())
    verify_JSON_object(request.result())

    return request.result().json()


def get_ratings(session, votesmart_id):
    """Returns a JSON response from the VoteSmart API"""
    payload = {'key': VOTE_SMART_API, 'candidateId': votesmart_id}
    request = session.get(
        'http://api.votesmart.org/Rating.getCandidateRating?&o=JSON',
        params=payload)

    # make sure we get a vaiid HTTP response and a JSON object
    verify_api_response(request.result())
    verify_JSON_object(request.result())

    return request.result().json()


def get_contributors(session, candidate_id):
    """Returns a JSON response from the Open Secrets API"""
    payload = {'cid': candidate_id, 'apikey': OPEN_SECRETS_API, 'cycle': 2016}
    request = session.get(
        'http://www.opensecrets.org/api/?method=candContrib&output=json',
        params=payload)

    verify_api_response(request.result())
    verify_JSON_object(request.result())

    return request.result().json()


def parse_stories(response):
    """Returns a list of NPRStory objects"""
    # create a list for storing NPRStory objects
    story_list = []
    # unpack the JSON response
    story_dict = response.get('list')
    list_of_stories = story_dict.get('story')
    # each story in the list is a dict
    try:
        for story in list_of_stories:
            # first get the url for the story
            story_url_list = story.get('link')
            url = story_url_list[0].get('$text')
            # then get the headline
            title_dict = story.get('title')
            title = title_dict.get('$text')
            npr_story = create_npr_story(url, title)
            story_list.append(npr_story)
    except TypeError:
        return story_list
        
    return story_list


def parse_ratings(response):
    """Returns a list of Rating objects"""
    # create a list for storing Rating objects
    ratings_list = []
    # unpack the JSON response
    candidate_rating_dict = response.get('candidateRating')
    list_of_ratings = candidate_rating_dict.get('rating')
    # each item in the list_of_ratings is a dict
    for rating_dict in list_of_ratings:
        # check the value of the rating
        try:
            # we only want ratings >=90 or 'A or B' rankings with ratingText
            if (int(rating_dict.get('rating')) >= 90) and rating_dict.get(
                'ratingText') and (rating_dict.get('timespan')
                                   in ['2016', '2015-2016']):
                rating = create_rating(rating_dict)
                ratings_list.append(rating)
        # sometimes the rating is A-F
        except ValueError:
            if(rating_dict.get('rating') in 'AB') and rating_dict.get(
                'ratingText') and (rating_dict.get('timespan')
                                   in ['2016', '2015-2016']):
                rating = create_rating(rating_dict)
                ratings_list.append(rating)
    return ratings_list


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


def create_npr_story(url, title):
    """Returns a NPRStory object with its values assigned"""
    # create a new NPRStory instance and assign the values
    npr_story = NPRStory(url=url, title=title)
    return npr_story


def create_rating(rating_dict):
    """Returns a Rating object with its values assigned"""
    # create a new Rating instance and assign its values from the dict
    rating = Rating(
        timespan=rating_dict.get('timespan'),
        rating_text=rating_dict.get('ratingText'),
        rating=rating_dict.get('rating')
        )
    return rating


def create_organization(attributes_dict):
    """Returns an Organization object with its values assigned"""
    # create a new organization instance and assign its values from the dict
    organization = Organization(
        name=attributes_dict.get('org_name'),
        total_contributed=attributes_dict.get('total'),
        pac_contributions=attributes_dict.get('pacs'),
        individual_contributions=attributes_dict.get('indivs')
        )
    return organization
