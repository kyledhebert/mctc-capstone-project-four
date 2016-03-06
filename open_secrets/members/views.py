from django.shortcuts import render

from .forms import StatePickerForm

from .utils import get_legislator_list


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


def legislator_list():
    pass
