#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
#import apiclient
from apiclient.discovery import build
import sys
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# https://developers.google.com/google-apps/calendar/quickstart/python
# json_file = '../../secret/nornv-f93fca6ecd4f.json'
json_file = '../../secret/nornv-141909-3dd642971fce.json'
scopes = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
http = httplib2.Http()
http_auth = credentials.authorize(http)
#service = apiclient.discovery.build("calendar", "v3", http=http_auth)
service = build("calendar", "v3", http=http_auth)
calendar_id = "ja.japanese#holiday@group.v.calendar.google.com"
dtfrom = date(year=2019, month=1, day=1).isoformat() + "T00:00:00.000000Z"
dtto   = date(year=2019, month=12, day=31).isoformat() + "T00:00:00.000000Z"
events_results = service.events().list(
        calendarId = calendar_id,
        timeMin = dtfrom,
        timeMax = dtto,
        maxResults = 50,
        singleEvents = True,
        orderBy = "startTime"
    ).execute()
events = events_results.get('items', [])

# 2019年は曖昧な特別な日が存在するので追加
events.append({
  'summary': 'Sample Event from Python',
  'start': {
    'date': '2019-05-01',
    'dateTime': '2019-05-01T00:00:00',
    'timeZone': 'Asia/Tokyo',
  },
  'end': {
    'date': '2019-05-01',
    'dateTime': '2019-05-01T23:59:59',
    'timeZone': 'Asia/Tokyo',
  },
  'recurrence': [],
})

reserve_doc_id = ['001','002','003']
reserve_times  = ['0900','0930','1000','1030','1100','1130']
reserve_times.extend(['1500','1530','1600','1630','1700','1730','1800'])
out_sql = "INSERT IGNORE INTO wl_ml.t_schedule VALUES \n"
out_sql_list  = []
print ("Content-Type: text/html;charset=utf-8")
print ("")
for event in events:
    print(" ## %s\t%s" % (event["start"]["date"], event["summary"]))
    for doc_id in reserve_doc_id:
        for a_time in reserve_times:
            out_sql_list.append("('%s','%s','%s',0,0,'root',now(),'root',now())" % (doc_id,event["start"]["date"],a_time))
out_sql += ",\n ".join(out_sql_list)
print("##-------------------SQL----------------")
print(out_sql)
print("##-------------------END----------------")
