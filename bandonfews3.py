#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Conor O'Neill using OAuth Code from Google
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
You need to setup Google API Access at https://code.google.com/apis/console/ and create a project there to get keys
Then put those keys in client_secrets.json
Also sudo pip install google-api-python-client to get the oAuth libraries installed
First time you run it with --noauth_local_webserver to do the OAuth authentication and save the AccessToken

Usage:
  $ python bandonfews3.py

"""

__author__ = 'cwjoneill@gmail.com (Conor O\'Neill)'
import gflags
import httplib2
import logging
import os
import pprint
import sys

import urllib
import lxml.html
from lxml.html.clean import clean_html
import time
import urllib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/fusiontables',
    message=MISSING_CLIENT_SECRETS_MESSAGE)


# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')


def main(argv):
  # Let the gflags module process the command-line arguments
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  # Set the logging according to the command-line flag
  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  # If the Credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('plus.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Scrape the Bandon FEWS webpage
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

  # now connect to Fusion Tables
  service = build("fusiontables", "v1", http=http)

  try:

    # Check to see if we have already recorded this level/time combination
    querystring = "SELECT * FROM 103YIcARoxuaWT7NfZ8mVBzY554sF_3ONYC1N3DE WHERE datetime='%s'" % datestring
    outcome = service.query().sql(sql=querystring).execute()
    print outcome
    if ('rows' not in outcome):
      # Insert latest River Level and Time
      querystring = "INSERT INTO 103YIcARoxuaWT7NfZ8mVBzY554sF_3ONYC1N3DE (riverlevel, datetime) VALUES ('%s', '%s')" % (riverlevel, datestring)
      outcome = service.query().sql(sql=querystring).execute()
      print outcome
    else:
      print "Already in database"
    print riverlevel
    print datestring

  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
