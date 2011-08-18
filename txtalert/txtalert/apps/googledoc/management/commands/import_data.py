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
                Setting.objects.get(name='THERAPYEDGE_USERNAME').value,
                Setting.objects.get(name='THERAPYEDGE_PASSWORD').value
            ),
            verbose=settings.DEBUG
        )
        for clinic in Clinic.objects.filter(active=True):
            # from midnight
            midnight = datetime.now().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            since = midnight - timedelta(days=1)
            # until 30 days later
            until = midnight + timedelta(days=30)
            print clinic.name, 'from', since, 'until', until
            try:
                for key, value in importer.import_all_changes(
                        User.objects.get(username='kumbu'),
                        clinic, 
                        since=since,
                        until=until
                    ).items():
                    print "\t%s: %s" % (key, len(value))
            except ExpatError, e:
                print "Exception during processing XML for clinic ", clinic
                traceback.print_exc()
            
            
        
                