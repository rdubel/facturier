from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^list/$', ProposalListView.as_view(), name='proposal-list'),
    url(r'^create/$', ProposalCreateView.as_view(), name='proposal_create'),
    url(r'^client/create/$', ClientCreateView.as_view(), name='create_client'),
    url(r'^client/details/(?P<pk>\d+)/$', ClientDetailView.as_view(), name='client_detail'),
    url(r'^details/(?P<pk>\d+)/$', ProposalDetailView.as_view(), name='proposal_detail'),
    url(r'^details/(?P<pk>\d+)/edit/$', ProposalUpdateView.as_view(), name='proposal_update'),
    url(r'^tobill/(?P<pk>\d+)/$', ProposalToBill, name="proposal_to_bill"),
    url(r'^archive/(?P<pk>\d+)/$', ProposalArchiving, name="archive_proposal"),
]
