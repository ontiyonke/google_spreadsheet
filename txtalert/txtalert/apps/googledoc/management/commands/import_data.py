from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings
from txtalert.apps.general.settings.models import DocSettings
from txtalert.apps.googledoc.importer import Importer
from txtalert.apps.googledoc.models import SpreadSheet
from txtalert.core.models import Patient, Visit
from xml.parsers.expat import ExpatError
import sys, traceback
import os.path
import optparse

class Command(BaseCommand):
    """
    """

    args = '[google spradsheet filename ...]'
    help = 'Can run as Cron job.'

    def handle(self, *args, **kwargs):
        importer = Importer(
            uri='https://docs.google.com' % (
                Setting.objects.get(name='GOOGLE_USERNAME').value,
                Setting.objects.get(name='GOOGLE_PASSWORD').value
            ),
            verbose=settings.DEBUG
        )
        for spreadsheet in SpreadSheet.objects.filter(active=True):
            try:
                importer.import_spread_sheet(spreadsheet)
            except ExpatError, e:
                print "Exception during processing XML for clinic ", clinic
                traceback.print_exc()
            
            
        
                