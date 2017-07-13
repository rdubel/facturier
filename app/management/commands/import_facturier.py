# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import csv
from app.models import *
from django.contrib.auth.models import User
from datetime import datetime


class Command(BaseCommand):
    help = "import shit"

    def handle(self, *args, **options):

        with open('app/management/commands/export_facturier.csv') as csvfile:
            readpls = csv.reader(csvfile, delimiter=';')
            readpls.next()
            check_list = []
            projid = 0

            for row in readpls:

                id, customer, status, creation_date, update_date, product, price, qty = row

                if id not in check_list:

                    check_list.append(id)

                    prop = Proposal(owner=User.objects.get(id=4),
                                    client=Client.objects.get(id=6),)
                    desc = id[:2]
                    if desc == "DV" and status == "STANDBY":
                        prop.status = Status.objects.get(id=1)
                    elif desc == "DV" and status == "LOST":
                        prop.status = Status.objects.get(id=2)
                    elif desc == "FA" and status == "STANDBY":
                        prop.status = Status.objects.get(id=3)
                    elif desc == "FA" and status == "PAID":
                        prop.status = Status.objects.get(id=4)

                    prop.creation_date = datetime.strptime(creation_date, "%d/%m/%y %H:%M")

                    if update_date:

                        prop.update_date = datetime.strptime(update_date, "%d/%m/%y %H:%M")

                    prop.save()
                    projid = prop.id

                    line = Service(proposal=Proposal.objects.get(id=projid))
                    line.service_name = product
                    line.unit_price = price
                    line.quantity = qty
                    line.save()

                    print "Project successfully created and line successfully added"

                else :

                    line = Service(proposal=Proposal.objects.get(id=projid))
                    line.service_name = product
                    line.unit_price = price
                    line.quantity = qty
                    line.save()

                    print "Line successfully created"
