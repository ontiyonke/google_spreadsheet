#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt
import sys
import string
import datetime
import re


class SimpleCRUD:

  def __init__(self, email, password):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Import Google SpreadSheet to Database'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = ''
    self.curr_wksht_id = ''
    self.list_feed = None
    
  def getSpreadsheet(self, doc_name):
    """Query the spreadsheet by name, and extract the unique spreadsheet ID."""
    self.doc_name = doc_name
    q = gdata.spreadsheet.service.DocumentQuery()
    q['title'] = self.doc_name
    q['title-exact'] = 'true'
    feed = self.gd_client.GetSpreadsheetsFeed(query=q)
    self.curr_key = feed.entry[0].id.text.rsplit('/',1)[1]
       
       
  def getWorksheets(self):
    """Acess the enrol and current month's worksheets of the current spread sheet."""
    print 'Inside getWorksheet current key is: %s\n' % self.curr_key
    #months tuple
    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    #get current month
    curr_month = datetime.date.today().month  
    curr_month = int(curr_month)
    # Get the list of worksheets
    feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
    #self._PrintFeed(feed)
    for i, entry in enumerate(feed.entry):
        #check for this month's worksheet
        if entry.title.text == 'enrollment sheet':
            print 'getting enrollment sheet'
            select = i
            id_parts = feed.entry[select].id.text.split('/')
            self.enrol_wksht_id = id_parts[len(id_parts) - 1]
            
        if datetime.date.today().day == 30 or datetime.date.today().day == 31:
            if months[curr_month] == entry.title.text:
                select = i
                id_parts = feed.entry[select].id.text.split('/')
                self.month_wksht_id = id_parts[len(id_parts) - 1]
        else:
            if months[curr_month-1] == entry.title.text:
                print 'print i from getworksheet: %s\n' % i
                select = i
                id_parts = feed.entry[select].id.text.split('/')
                #print id_parts
                self.month_wksht_id = id_parts[len(id_parts) - 1]
                
           
  def _PromptForListAction(self):
    self._ListGetAction()
    
  def _ListGetAction(self):
    # Get the list feed
    list_feed = self.gd_client.GetListFeed(self.curr_key, self.enrol_wksht_id)
    #self._PrintFeed(feed)
    #get the enrollment worksheet
    enrol_sheet = self.processFile(list_feed)
    
  def _PromptForCellsAction(self):
      self._CellsGetAction()
      
  def _CellsGetAction(self):
    # Get the feed of cells
    feed = self.gd_client.GetCellsFeed(self.curr_key, self.month_wksht_id)
    #self._PrintFeed(feed)
    #get the appointment worksheet 
    appointment = self.processFile(feed)  
       
  def processFile(self, feed):
    #list to store all the data inside the spreadsheet    
    rowList = []
        
    #list to stores other lists which will store each row in spreadsheet
    tableLists = []   
    
    #stores the total number of rows in the spreadsheet
    numOfRows = 0
        
    #stores the total number of columns in the spreadsheet
    numOfCols = 0
    
    #process this month's appointment data
    if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
        feed_type = 'cells'
        print 'working on this month\n'
        app_work = []
        app_worksheet = {}
        q = gdata.spreadsheet.service.CellQuery()
        #totalRows = q._GetMaxResults()
        #print totalRows
        #totalColums = gdata.spreadsheet.ColCount()
        #totalRows = gdata.spreadsheet.RowCount()
        
        #print totalRows
        #loop through all the rows in the data
        for i, entry in enumerate(feed.entry):
            #store the appointmnet worksshet in dictionary the key is the cell's id and value is cell value
            temp_dic = {entry.title.text:entry.content.text}
            #print temp_dic
            app_work.append(temp_dic)
            #app_worksheet.update(temp_dic)
            temp_dic = {}
            
            #print '%s %s\n' % (entry.title.text, entry.content.text)
        #app_work.reverse()
        print app_work
        
        '''for k, v in row_data.iteritems():
            new_custom = gdata.spreadsheet.Custom()
            new_custom.column = k
            new_custom.text = v
            new_entry.custom[new_custom.column] = new_custom'''
        #print app_work
        #self.getRow(app_dic, columns, totalRows, feed) 
        #print app_work
            #totalRows = totalRows + 1
            #print 'total rows in the worksheet are: %d' % totalRows
            #get the number of columns per row
            #colsPerRow =
        #for k, v in sorted(app_worksheet.items()):
            #print (k, v)
            #if 
        #new_worksheet =  sorted(app_worksheet.items())
        #print app_worksheet
        #get rows from appointment worksheet
        #app_worksheet = self.getRow(app_worksheet, colsPerRow, totalRows, feed_type)              
                
        #return app_worksheet
            #store the row in a dictionary
            #for each_col in range
           
    #process enrollment worksheet        
    elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        feed_type = 'list'
        print 'working on enrol\n'
        enrol_patient = {}
        enronl_worksheet = {}
        temp_dic = {}
        tempdic = {}
        copydic = {}
        #loop through all the rows in the data
        for i, entry in enumerate(feed.entry):
            row_no = i
            for key in entry.custom:
                #create a dictionary to store a row in worksheet
                temp_dic = {key:entry.custom[key].text}
                tempdic.update(temp_dic)
                temp_dic = {}
            copydic = {row_no:tempdic}
            enrol_patient.update(copydic)
            
            copydic = {}
            tempdic ={}
        #for each row get proper type for each one of its contents
        for k in enrol_patient:
            row_no = k + 2
            #get proper values for each key in row dictionary
            enrol_p = self.databaseRecord(enrol_patient[k], feed_type)
            enroltemp = {k:enrol_p} 
            enrol_p = {}
            #dictionary that stores a row number as a key to the row data  
            enronl_worksheet.update(enroltemp)
            enroltemp = {}
             
            row_no = 0
        return enronl_worksheet
        
   
  
  def getRow(self, app_dic, columns, totalRows, feed):
      #used to construct a dictionary with key being the data row number
      temp_dic = {}
      #stores the worksheet row data
      row_dic = {}
      #stores the worksheet rows
      app_worksheet = {}
      app_dic_temp = app_dic
      #store the current row value
      t_rows = 0
      
      #create a list that contains data for a single row/record
      for each_value in range(len(app_dic_temp)):
          #check if row_dic does not consists of a row
          if len(row_dic) < colums:
              pass
              #save current value to row data
              #row_dic.append(dList.pop())
           
          #check if the list contains an entire row's data if true return list            
          elif len(row_dic) == colums:
              if t_rows <= totalRows:
                  #get proper type for each value in the row dictionary
                  row_dic = self.databaseRecord(row_dic, feed)
                  #get current row number
                  t_rows = t_rows + 1
                  #create a dictionary with key being the row number and value being a dictionary with row content
                  temp_dic = {t_rows:row_dic}
                  #create dictionary to store the worksheet rows
                  app_worksheet.update(temp_dic)
                  #clear work dictionary for re-use
                  temp_dic = {}
                  row_dic = {}
                             
          #if app_dic_temp has more than one row call getRow to proces all the rows
          else:
              self.getRow(app_dic_temp, columns, totalRows, feed)
             
      #returns worhsheet
      return app_worksheet
   
  def dateObjectCreator(self, datestring):
      dateformat = '%d/%m/%Y'
      try:
          real_date = datetime.datetime.strptime(datestring, dateformat)
          real_date = real_date.date()
          return real_date
      except TypeError:
          return TypeError
 
  def databaseRecord(self, dic, feed):
      
      if feed == 'list':
          enrol_dic = dic
          enrolDic = {}          
          for key in enrol_dic:
              #check if this is patient ID and convert it to proper type value
              if key == 'patientid':
                  #print 'inside databaseRecord patientid check\n'
                  try:
                      temp_dic = {key:int(enrol_dic[key])}
                      enrolDic.update(temp_dic) 
                      temp_dic = {}
                  except TypeError:
                      temp_dic = {key:TypeError}
                      enrolDic.update(temp_dic) 
                      temp_dic = {}                 
              elif key == 'patientfileno':
                  #print 'inside databaseRecord patientfileno check\n'
                  try:
                      temp_dic = {key:int(enrol_dic[key])}
                      enrolDic.update(temp_dic) 
                      temp_dic = {}
                  except TypeError:
                      temp_dic = {key:TypeError}
                      enrolDic.update(temp_dic) 
                      temp_dic = {} 
              elif key == 'patientphonenumber':
                  try:
                      #print 'inside databaseRecord patientphonenumber check\n'
                      temp_dic = {key:int(enrol_dic[key])}
                      enrolDic.update(temp_dic) 
                      temp_dic = {}
                  except ValueError:
                      temp_dic = {key:ValueError}
                      enrolDic.update(temp_dic) 
                      temp_dic = {} 
              elif key == 'dateofenrollment':
                  #print 'inside databaseRecord patientidcheck\n'
                  enrol_date = self.dateObjectCreator(enrol_dic[key])
                  temp_dic = {key:enrol_date}
                  enrolDic.update(temp_dic)
                  temp_dic = {}
      
      elif feed == 'cells':
          app_dic = dic
          appDic = {}
          for key in app_dic:
              #check if this is patientid and convert it to proper type value
              if key == 'File no':
                  try:
                      appDic.update(key=int(app_dic[key])) 
                  except TypeError:
                      appDic.update(key=TypeError)
              elif key == 'Phone Number':
                  try:
                      appDic.update(key=int(app_dic[key]))
                  except TypeError or ValueError:
                      if TypeError:
                          enrolDic.update(key=TypeError)
                      elif ValueError:
                          enrolDic.update(key=ValueError)
              elif key == 'Appointment date 1':
                  app_date = self.dateObjectCreator(app_dic[key])
                  appDic.update(key=app_date)
              elif key == 'Appointment Status 1':
                  try:
                      appDic.update(key=app_dic[key]) 
                  except TypeError:
                      appDic.update(key=TypeError)
                      
      if enrolDic:
          return enrolDic
      elif appDic:
          return appDic
                  
  def Run(self, doc_name='ByteOrbit copy of WrHI spreadsheet for Praekelt TxtAlert', row_no=3):
    """Expects the name of the spreadsheet to be imported as well as the row numnber to start exxporting from."""
    #get the spread sheet to be worked on
    self.getSpreadsheet(doc_name)
    #get the worksheets on the spreadsheet
    self.getWorksheets()
    #get the enrollment data use list
    #enrol_worksheet = self._PromptForListAction()
    #get data from this month's worksheet use cells
    month_worksheet = self._PromptForCellsAction()
    
    #return (enrol_worksheet, month_worksheet)
    

def main():
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["user=", "pw="])
  except getopt.error, msg:
    print 'python spreadsheetReader.py --user [username] --pw [password] '
    sys.exit(2)
  
  user = ''
  pw = ''
  key = ''
  # Process options
  for o, a in opts:
    if o == "--user":
      user = a
    elif o == "--pw":
      pw = a
   
     

  if user == '' or pw == '':
    print 'python spreadsheetExample.py --user [username] --pw [password]'
    sys.exit(2)
        
  sample = SimpleCRUD(user, pw)
  sample.Run()


if __name__ == '__main__':
  main()
