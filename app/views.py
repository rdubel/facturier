# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import transaction

from .models import *
from .forms import ProposalInlineFormSet

# Create your views here.
class ProposalListView(ListView):

    model = Proposal

class ProposalDetailView(DetailView):

    model = Proposal
    pk_field = "id"

    def services(self):

        return Service.objects.filter(proposal=self.object.id)

class ProposalCreateView(CreateView):

    model = Proposal
    fields = "__all__"

    def line(self):
        if self.request.POST:
            return ProposalInlineFormSet(self.request.POST)
        else:
            return ProposalInlineFormSet()

    def form_valid(self, form):

        lines = self.line()
        proposal = form.save()

        if lines.is_valid():

            lines.instance = proposal
            lines.save(form)

        return super(ProposalCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('proposal_detail', kwargs={'pk' : self.object.id})


class ProposalUpdateView(UpdateView):
    model = Proposal
    fields = "__all__"

    def line(self):
        if self.request.POST:
            return ProposalInlineFormSet(self.request.POST)
        else:
            return ProposalInlineFormSet(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super(ProposalUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['serviceline'] = ProposalInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['serviceline'] = ProposalInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        serviceline = context['serviceline']
        with transaction.atomic():
            self.object = form.save()
        if serviceline.is_valid():
            serviceline.instance = self.object
            serviceline.save()
        return super(ProposalUpdateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('proposal_detail', kwargs={'pk' : self.object.id})

class ClientCreateView(CreateView):
    model = Client
    fields = "__all__"

    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk' : self.object.id})

class ClientDetailView(DetailView):

    model = Client
    pk_field = "id"

    def proposals(self):
        return Proposal.objects.filter(client=self.object)
