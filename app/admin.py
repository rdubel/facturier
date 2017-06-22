# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

class ServiceInline(admin.TabularInline):
    model = Service
    can_delete = True
    verbose_name_plural = "Products"

class ProposalAdmin(admin.ModelAdmin):
    inlines = (ServiceInline,)

admin.site.register(Client)
admin.site.register(Status)
admin.site.register(Proposal, ProposalAdmin)
