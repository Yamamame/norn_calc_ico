#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import apiclient
import sys
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# https://developers.google.com/google-apps/calendar/quickstart/python
json_file = '../../secret/nornv-f93fca6ecd4f.json'
scopes = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
http = httplib2.Http()
http_auth = credentials.authorize(http)
service = apiclient.discovery.build("calendar", "v3", http=http_auth)
calendar_id = "ja.japanese#holiday@group.v.calendar.google.com"
dtfrom = date(year=2017, month=1, day=1).isoformat() + "T00:00:00.000000Z"
dtto   = date(year=2017, month=12, day=31).isoformat() + "T00:00:00.000000Z"
events_results = service.events().list(
        calendarId = calendar_id,
        timeMin = dtfrom,
        timeMax = dtto,
        maxResults = 50,
        singleEvents = True,
        orderBy = "startTime"
    ).execute()
events = events_results.get('items', [])
print "Content-Type: text/html;charset=utf-8"
print ""
for event in events:
    print("%s\t%s" % (event["start"]["date"], event["summary"]))
print("END")
