#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Conor O'Neill 
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

Command-line application that grabs river level data from the Bandon FEWS site and stores it in Pachube/Cosm

Usage:
  $ python fews2cosm.py

"""

__author__ = 'cwjoneill@gmail.com (Conor O\'Neill)'


import urllib
import lxml.html
from lxml.html.clean import clean_html
import time
import sys, urllib2


if __name__ == "__main__":

  import sys, getpass

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
      
      #Push to Cosm/Pachube every time even if not updated
      apiKey = "insertyourshere"
      feedID = "40004"
      putdata="""
        {
          "version":"1.0.0",
          "datastreams":[
            {"id":"1", "current_value":"%s"}
           ]
         } """ % riverlevel
      opener = urllib2.build_opener(urllib2.HTTPHandler)
      request = urllib2.Request('http://api.cosm.com/v2/feeds/'+feedID+'?_method=put', putdata)
      request.add_header('X-ApiKey', apiKey)
      cosmurl = opener.open(request)

