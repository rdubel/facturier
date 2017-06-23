from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^list/$', ProposalListView.as_view(), name='proposal-list'),
    url(r'^details/(?P<pk>\d+)/$', ProposalDetailView.as_view(), name='proposal_detail'),
    url(r'^create/', ProposalCreateView.as_view(), name='proposal_create')
]
