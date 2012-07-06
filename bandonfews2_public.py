#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Conor O'Neill using OAuth Code from Google
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

"""Simple command-line to scrape Bandon FEWS

Command-line application that grabs river level data from the Bandon FEWS site and stores it in Google Fusion Tables

Usage:
  $ python bandonfews2.py

"""

__author__ = 'cwjoneill@gmail.com (Conor O\'Neill)'


from sql.sqlbuilder import SQL
import ftclient
from fileimport.fileimporter import CSVImporter

import urllib
import lxml.html
from lxml.html.clean import clean_html
import time
import sys, urllib2


if __name__ == "__main__":

  import sys, getpass

  consumer_key = 'insertyourshere'
  consumer_secret = 'insertyourshere'

  oauth_client = ftclient.OAuthFTClient(consumer_key, consumer_secret)

  url = 'http://www.bandonfloodwarning.ie/main.php'
  html = urllib.urlopen(url).read()

  root = lxml.html.fromstring(html)
  roottext = root.text_content()

  sentences = roottext.split('\r\n')

  
  for j in sentences:
    if j.rfind('Water Level (m) at Bandon Bridge Gauge:') != -1:
      currenttext = j
      level = currenttext.lstrip('Water Level (m) at Bandon Bridge Gauge:    ')
      level = level.strip()
      when = level
      level = level.split(' ')
      riverlevel = float(level[0])
      when = when.split('Last Update:')
      datetime = when[1]
      in_time_format = "%A, %d %b. %Y at %H:%M %Z"
      datetime = time.strptime(datetime,in_time_format)
      out_time_format = "%d-%b-%Y %H:%M"
      datestring = time.strftime(out_time_format, datetime)
      
  #create a table
  #  table = {'FEWS2':{'riverlevel':'NUMBER', 'datetime':'DATETIME'}}
  #  tableid = int(oauth_client.query(SQL().createTable(table)).split("\n")[1])
  #  print tableid
      querystring = "datetime=" + "'" + datestring + "'"
      result = oauth_client.query(SQL().select(2191951, None, querystring))
      if (result.find(datestring) == -1):
        #insert row into table
        rowid = int(oauth_client.query(SQL().insert(2191951, {'riverlevel': riverlevel, 'datetime': datestring})).split("\n")[1])
        print riverlevel + " , " + datestring
