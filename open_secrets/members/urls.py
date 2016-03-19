from django.conf.urls import url

from . import views

app_name = 'members'
urlpatterns = [
    # both urls point to the member detail view
    # one does not require a votesmartId
    url(r'^(?P<candidate_name>[a-zA-z -]+)/'
        '(?P<candidate_id>N[0-9]+)/$',
        views.member_detail, name='member_detail'),
    # one does, this allows us to list candidates without a votesmart id
    # on the results page
    url(r'^(?P<candidate_name>[a-zA-z -]+)/'
        '(?P<candidate_id>N[0-9]+)/(?P<votesmart_id>[0-9]+)/$',
        views.member_detail, name='member_detail'),
    url(r'^save/$',
        views.save_member_details, name='save_member_details'),
]
