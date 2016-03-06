from django.shortcuts import render

from .forms import StatePickerForm

from .utils import get_legislator_list, get_contributors_list


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


def member_detail(request, candidate_id):
    # query the Open Secrets API to get a list of contributors
    contributors_list = get_contributors_list(candidate_id)

    return render(request, 'members/member_detail.html', {
        'contributors_list': contributors_list,
        })
