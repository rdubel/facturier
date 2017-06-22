# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.
class ProposalListView(ListView):

    model = Proposal

class ProposalDetailView(DetailView):

    model = Proposal
    pk_field = "id"

    def services(self):

        return Service.objects.filter(proposal=self.object.id)
