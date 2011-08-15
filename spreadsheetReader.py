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
        '''print 'Inside for loop current month: %s worksheet month: %s\n' % (months[curr_month-1], entry.title.text)
        print 'Inside for loop current month: %s\n' % (months[curr_month-1])
        print 'Inside for loop current month data type : %s\n' % (type(months[curr_month-1]))
        print 'Inside for loop worksheet month: %s\n' % (entry.title.text)
        print 'Inside for loop worksheet month data type: %s\n' % (type(entry.title.text))'''
            
        if entry.title.text == 'enrollment sheet':
            print 'getting enrollment sheet'
            select = i
            id_parts = feed.entry[select].id.text.split('/')
            self.enrol_wksht_id = id_parts[len(id_parts) - 1]
            
        elif months[curr_month-1] == entry.title.text:
            '''print 'equal months'
            get current month's worksheet'''
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
        #loop through all the rows in the data
        for i, entry in enumerate(feed.entry):
            rowList.append(entry.content.text)
            
        #reverse the list values to prepare for extraction   
        tableLists.reverse()
    
        #call function to extract a row data and assign it to list that contain lists of rows 
        tableLists = self.getRow(tableLists, numOfCols, feed_type)
                
    #process enrollment worksheet        
    elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        feed_type = 'list'
        print 'working on enrol\n'
        #loop through all the rows in the data
        for i, entry in enumerate(feed.entry):
            #confirm that i represents the row number
            numOfRows =  numOfRows + i
            numOfCols = len(entry.custom)
            for key in entry.custom:
                #append the current cell value to the list
                rowList.append(entry.custom[key].text)
                
            #if the entry consist of a single row
            #nsert the row number as first value in list
            rowList.insert(0, i+2)
            tableLists.append(rowList)
            rowList = []
        #get proper types for each row value
        tableLists = self.databaseRecord(tableLists, feed_type)             
        #print tableLists
    #return 2D table list: the lists inside this list consist of the table rows
    return tableLists 
    
   
  def getRow(self, dList, tCols, feed):
    """Expects a list that contains all the info in the spreadsheet as well as the total number of columns
    for a row in the spreadsheet. Returns a 2D List"""
    #list to stores a single row/record data
    rowList = []
    #stores the argument list for local use
    tempList = []

    #stores list that contains list(s)
    list_2D = []
    
    #stores the argument total number of colums in the spreadsheet for local use
    totalCols = tCols
    
    #create a list that contains data for a single row/record
    for each_value in range(len(dList)):
        #check if rowList does not consists of a row
        if len(rowList) < totalCols:
            #save current value to row data
            rowList.append(dList.pop())
           
        #check if the list contains an rntire row's data if true return list            
        if len(rowList) == totalCols:
            list_2D.append(rowList)
            rowList = []
                             
        #if tempList has more than one row call getRow to proces all the rows
        else:
            self.getRow(tempList, totalCols, feed)

    list_2D = self.databaseRecord(list_2D, feed)
    #returns a 2D list
    return list_2D
            
  
    
  def dateObjectCreator(self, datestring):
      dateformat = '%d/%m/%Y'
      real_date = datetime.datetime.strptime(datestring, dateformat)
      real_date = real_date.date()
       

  def databaseRecord(self, table_list, feed_type):
    row = []
    table = []
           
    #loop through customer table to access each row
    for each_row in table_list:
        #convert the data from this month's appointment worksheet to their proper type's
        if feed_type == 'cells':
            app_date = self.dateObjectCreator(each_row[2])
            #patient's file number
            row.append(int(each_row[0]))
            #patient's phone number
            row.append(int(each_row[1]))
            #Appointment date
            row.append(app_date)
            #Appiontment status
            row.append(each_row[3])
            #Appointment attend date
            if each_row[4]:
                att_date = self.dateObjectCreator(each_row[4])
                row.append(att_date)
      
        #convert the data from the enrollment to its proper type          
        if feed_type == 'list': 
            app_date = self.dateObjectCreator(each_row[4])
            #patient ID            
            row.append(int(each_row[3]))
            #patient file number
            try:
                row.append(int(each_row[1]))
            except TypeError:
                #print no file name error in the output log.
                print TypeError
            try:
                #patient phone number            
                row.append(each_row[2])
            except ValueError:
                #print no file name error in the output log.
                print ValueError
        
                #patient's date of enrollment
                row.append(app_date)
        
        print table 
        #create table
        table.append(row)
            
    #return the table                  
    return table  
 
  def _PrintFeed(self, feed):
    for i, entry in enumerate(feed.entry):
      if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
        print '%s %s %s\n' % (entry.title.text, type(entry.content.text), entry.content.text)
      elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
        print '%s %s %s' % (i, entry.title.text, entry.content.text)
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        print '\nContents: %s\n\n' % entry.content.text
        print 'Contents:'
        for key in entry.custom:  
          print '  %s: %s' % (key, entry.custom[key].text) 
        print '\n',
      else:
        print '%s %s\n' % (i, entry.title.text)
  

  def Run(self):
    #get the spread sheet to be worked on
    self.getSpreadsheet('ByteOrbit copy of WrHI spreadsheet for Praekelt TxtAlert')
    #get the worksheets on the spreadsheet
    self.getWorksheets()
    #get the enrollment data use list
    enrol_worksheet = self._PromptForListAction()
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
