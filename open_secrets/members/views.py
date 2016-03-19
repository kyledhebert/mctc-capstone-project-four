import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import StatePickerForm

from .models import Legislator

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
# won't have a votesmart candidate_id
def member_detail(request, candidate_name, candidate_id, votesmart_id=0):
    # store the args in the session so users can save the results  
    request.session['candidate_name'] = candidate_name
    request.session['candidate_id'] = candidate_id
    request.session['votesmart_id'] = votesmart_id
    
    # get a dict of member details by querying the OpenSecrets,
    # VoteSmart, and NPR APIs
    member_details_dict = get_details_dict(candidate_name,
                                           candidate_id, votesmart_id)

    # unpack the dictionary to create the lists
    contributors_list = member_details_dict.get('contributors')
    npr_story_list = member_details_dict.get('stories')

    if 'ratings' in member_details_dict:
        ratings_dict = member_details_dict.get('ratings')
        good_ratings_list = ratings_dict.get('good_ratings')
        bad_ratings_list = ratings_dict.get('bad_ratings')

        return render(request, 'members/member_detail.html', {
            'candidate_name': candidate_name,
            'contributors_list': contributors_list,
            'good_ratings_list': good_ratings_list,
            'bad_ratings_list': bad_ratings_list,
            'npr_story_list': npr_story_list
        })
    else:
        return render(request, 'members/member_detail.html', {
            'candidate_name': candidate_name,
            'contributors_list': contributors_list,
            'npr_story_list': npr_story_list
        })


def save_member_details(request):
    # first get or create a new Legislator entry in the DB
    legislator, created = Legislator.objects.get_or_create(
        name=request.session['candidate_name'],
        candidate_id=request.session['candidate_id'],
        votesmart_id=request.session['votesmart_id'],
        )
    # then update the legislator to include the user
    # because saved_by is a ManytoMany field the legislator
    # has to be saved() before we can assoicate users
    legislator.saved_by.add(request.user)

    # delete the session values once the details are saved
    del request.session['candidate_name']
    del request.session['candidate_id']
    del request.session['votesmart_id']

    return HttpResponseRedirect(reverse('home'))
