# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Client(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Status(models.Model):

    status = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Statuses"

    def __unicode__(self):
        return self.status


class Proposal(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(null=True, blank=True)
    update_date = models.DateTimeField(null=True, blank=True)

    def amount(self):
        result = 0
        for service in self.service_set.all():
            result += service.unit_price * service.quantity
        return result

    def __unicode__(self):
        return self.status.status + " - " + self.owner.username + " - " + self.client.last_name + " | id : " + str(self.id)


class Service(models.Model):

    service_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.SmallIntegerField()
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)

    def service_price(self):
        return self.unit_price * self.quantity

    def __unicode__(self):
        return self.service_name
