from django.conf.urls import url

from . import views

app_name = 'members'
urlpatterns = [
    url(r'^(?P<candidate_id>N[0-9]+)/(?P<votesmart_id>[0-9]+)/$',
        views.member_detail, name='member_detail')
]
