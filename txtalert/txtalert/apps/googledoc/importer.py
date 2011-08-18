from django.db import IntegrityError
from txtalert.apps.googledoc.xmlrpc.client import Client
from txtalert.core.models import Patient, MSISDN, Visit, Clinic

import iso8601
import re
import logging
from datetime import datetime, date

from django.db import IntegrityError
from txtalert.apps.therapyedge.xmlrpc.client import Client
from txtalert.core.models import Patient, MSISDN, Visit, Clinic

import iso8601
import re
import logging
from datetime import datetime, date

logger = logging.getLogger("importer")

PATIENT_ID_RE = re.compile(r'^[0-9]{2}-[0-9]{5}$')
PATIENT_FILE_NO_RE = re.compile(r'^[0-9]{1,3}$')
PATIENT_PHONE_RE = re.compile(r'^(Male|Female|Transgender ?(f->m|m->f)?)$')

APPOINTMENT_ID_RE = re.compile(r'^[0-9]{2}-[0-9]{9}$')
DATE_RE = re.compile(r'^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}$')

MSISDNS_RE = re.compile(r'^([+]?(0|27)[0-9]{9}/?)+$')
MSISDN_RE = re.compile(r'[+]?(0|27)([0-9]{9})')

IMPORT_CUTOFF = datetime(2009, 01, 01)
IMPORT_DAY_INTERVAL = 10

MESSAGE_PATIENTID_INCONSISTENT = "Patient ID '%s' is inconsistent with previous ID '%s' for visit '%s'."
MESSAGE_PATIENT_NOTFOUND = "Patient with the ID '%s' could not be found for visit '%s'."
MESSAGE_VISIT_NOTFOUND = "Visit with the ID '%s' could not be found."

class Importer(object):
    def __init__(self, uri=None, verbose=False):
        self.client = Client(uri, verbose)

    def import_spreadsheet(self, username, password, doc_name):
        #get the last imported row number from database
        startRow = RowNumber.objects.all()
        startRow = startRow + 1
        #start cron job to get the clerk's spread sheet data
        reader = SimpleCRUD(username, password)
        #run job to get current clerk's data
        (month, enrol) = reader.Run(doc_name, startRow)
    

    def updatePatientInfo(month):
        
       
    def updateAppointment(rowlist):
        """Updates the existing patient appointment information."""
        
        #use patient's unique id and row number on spreadsheet to find the patient database record
        curr_patient = Visit.objects.filter(te_visit_id=)
                    
        #check if the user has attended the scheduled appointment    
        if app_status == 'Attended':
            #if the appointment was scheduled or rescheduled transform it to attened
            if curr_patient.status == 'Scheduled' or curr_patient.status == 'Rescheduled':
                curr_patient.status = 'Attended'    
        #if the user has missed a scheduled or rescheduled appointment
        elif app_status == 'Missed':
            if curr_patient.status == 'Scheduled' or curr_patient.status == 'Rescheduled':
                curr_patient.status = 'Missed'
        #check if the patient has rescheduled 
        elif app_status = 'Rescheduled' and curr_patient.status == 'Scheduled':
            curr_patient.status = 'Rescheduled'    
            
    def enrolPatient(enrolList):
        """Used to enrol a patient """
        for each_enrol in enrolList:
            #get the unique identifier
            row_no = each_enrol[0]
            file_no = each_enrol[1]
            #use patient's unique id and row number on spreadsheet to find the patient database record
            curr_patient = Patient.objects.filter(te_visit_id=)
            #check if the user has not been previously enrolled 
            if len(curr_patient) == 0:
                #if the patient does not exists create new enrollment
                enrol = Patient
            elif:
                #update the patientenrol info (get the name of the table to enrol patient to )
                update_enrol = Patient()
        
    