from django.shortcuts import render

from .forms import StatePickerForm

from .utils import get_legislator_list, get_details_dict


def index(request):
    # if this is a POST request, process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = StatePickerForm(request.POST)
        # check whether the form is valid 
        if form.is_valid():
            # use the state picked in the form to complete the api query
            # and generate a list that gets passed to render
            state = {form.cleaned_data['state']}
            legislator_list = get_legislator_list(state)
            
    # if this is a GET create a blank form
    else:
        form = StatePickerForm() 
        legislator_list = []
    return render(request, 'layouts/index.html', {
        'form': form,
        'legislator_list': legislator_list
        })


# a default value for votesmart id gets passed since all members 
# won't have a votesmart id
def member_detail(request, candidate_name, candidate_id, votesmart_id=0):
    # get a dict of member details by querying the OpenSecrets,
    # VoteSmart, and NPR APIs
    member_details_dict = get_details_dict(candidate_name,
                                           candidate_id, votesmart_id)

    # unpack the dictionary to create the lists
    contributors_list = member_details_dict.get('contributors')
    ratings_dict = member_details_dict.get('ratings')
    good_ratings_list = ratings_dict.get('good_ratings')
    bad_ratings_list = ratings_dict.get('bad_ratings')
    npr_story_list = member_details_dict.get('stories')

    return render(request, 'members/member_detail.html', {
        'candidate_name': candidate_name,
        'contributors_list': contributors_list,
        'good_ratings_list': good_ratings_list,
        'bad_ratings_list': bad_ratings_list,
        'npr_story_list': npr_story_list
        })
