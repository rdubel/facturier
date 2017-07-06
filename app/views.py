# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import transaction
from django.http import Http404

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
    fields = ['client']

    def line(self):
        if self.request.POST:
            return ProposalInlineFormSet(self.request.POST)
        else:
            return ProposalInlineFormSet()

    def usage(self):
        return "create"

    def form_valid(self, form):

        lines = self.line()
        form.instance.owner = self.request.user
        form.instance.status = Status.objects.get(id=1)
        proposal = form.save()

        if lines.is_valid():

            lines.instance = proposal
            lines.save(form)

        return super(ProposalCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('proposal_detail', kwargs={'pk' : self.object.id})


class ProposalUpdateView(UpdateView):
    model = Proposal
    fields = ['client']

    def usage(self):
        return "update "


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

def ProposalToBill(request, pk):

    project = Proposal.objects.get(id=pk)
    if project:
        project.status = Status.objects.get(id=3)
        project.save()
        return redirect('proposal_detail', pk=pk)
    else:
        raise Http404("this project does not exist")


def ProposalArchiving(request, pk):

    project = Proposal.objects.get(id=pk)
    if project:
        project.status = Status.objects.get(id=2)
        project.save()
        return redirect('proposal_detail', pk=pk)
    else:
        raise Http404("this project does not exist")
