from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from views import LoginForm
from cron import RetriveSpreadSheet, main
form spreadsheetReader import SimpleCRUD

def google_details(request):
    if request.method == 'POST':
        googleForm = LoginForm(request.POST)
        if googleForm.is_valid():
            username=googleForm.cleaned_data['username']
            password=googleForm.cleaned_data['password']
            #find a way to send this info to main in cron
            import_spreadsheet(request, username, password)
    else:
        googleForm = LoginForm()
        
    context = RequestContext(request)
    
    return render_to_response('import/import_spreadsheet.html', {'form': googleForm}, context_instance=context)
    

def import_spreadsheet(request, username, password):
    #start cron job to get the clerk's spread sheet data
    reader = RetriveSpreadSheet()
    #run job to get current clerk's data
    reader.job(username, password)
    #redirect to a page to view the data
    #return HttpResponseRedirect('')
    
def updateAppointment(rowlist):
    """Updates the existing patient appointment information."""
    #extract patient unique id and row number from incoming list
    row_no = rowList[0]
    file_no = rowList[1]
    app_date = rowList[3]
    app_status = rowList[4]
    att_date = rowlist[5]
    #use patient's unique id and row number on spreadsheet to find the patient database record
    curr_patient = Visit.objects.filter(te_visit_id=)
    
    """ use this if the clerks makes modification of date
    #check if the appointment date is the same as the one stored on the database
    if curr_patient.date == app_date:
        #check if the user has attended the scheduled appointment    
        if app_status == 'Attended':
            #if the appointment was scheduled or rescheduled transform it to attened
            if curr_patient.status == 'Scheduled' or curr_patient.status == 'Rescheduled'
            curr_patient.status = 'Attended'
        
        #if the user has missed a scheduled or rescheduled appointment
        elif app_status == 'Missed':
            curr_patient.status = 'Missed'
            
    #check if the date is in the future and reschedule appointment if so
    elif curr_patient.date < app_date:
        #check if the patient has rescheduled 
        if app_status = 'Rescheduled' and curr_patient.status == 'Scheduled':
            curr_patient.status = 'Rescheduled'"""
            
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
        #get the unique identifier (must figure out what the unique identifier is)
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
    
    

def saveRow(rowList):
    """Accepts a customer row to save to database"""
    c_row = []
    columns_field = []
    c_row = rowList
    
    c_row.reverse()
    columns_field = c_row.pop()
    c_row.reverse()
    
    #access the rows in the table
    for each_row in c_row:
        #store the row in the database
        for index in range(len(each_row)):
            #create a customer object
            customer = Customer(customer_id=each_row[0], january=int(each_row[1]), february=int(each_row[2]), march=int(each_row[3]), april=int(each_row[4]), may=int(each_row[5]), june=int(each_row[6]),
			july=int(each_row[7]), august=int(each_row[8]), september=int(each_row[9]), october=int(each_row[10]), november=int(each_row[11]), december=int(each_row[12]))     
        #save customer to Customers table in database 
        customer.save()    
