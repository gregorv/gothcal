#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Main file for generating the calendar file.

 Copyright 2012 Gregor Vollmer

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import culteum, nachtwerk, schwimmbad
import hashlib
from datetime import timedelta

def generateVCalendar(event_list):
    calendar =  "BEGIN:VCALENDAR\r\n"
    calendar += "PRODID:-//K Desktop Environment//NONSGML KOrganizer 4.4.5//EN\r\n"
    calendar += "VERSION:2.0\r\n"
    calendar += "CALSCALE:GREGORIAN\r\n"
    
    calendar += "BEGIN:VTIMEZONE\r\n"
    calendar += "TZID:Europe/Berlin\r\n"
    calendar += "END:VTIMEZONE\r\n"
    
    for date, url, name, description, club in event_list:
        id = 0
        print(name,date)
        dtstart = date.strftime('%Y%m%d')
        dtend = (date+timedelta(1)).strftime('%Y%m%d')
        
        calendar += "BEGIN:VEVENT\r\n"
        calendar += "UID:{0}{1}@gothcal.dynamic-noise.net\r\n".format(hashlib.md5(name.encode('utf-8')).hexdigest(), dtstart)
        calendar += "SUMMARY:"+name+"\r\n"
        
        #calendar += "DESCRIPTION:"
        #calendar += unicode(description)+"\\n\\n"
        #calendar += "\r\n"
        
        calendar += "DTSTART;VALUE=DATE:"+dtstart+"\r\n"
        calendar += "DTEND;VALUE=DATE:"+dtend+"\r\n"
        calendar += "URL:"+url+"\r\n"
        calendar += "LOCATION:"+club+"\r\n"
        calendar += "STATUS:CONFIRMED\r\n"
        calendar += "TRANSP:OPAQUE\r\n"
        
        calendar += "END:VEVENT\r\n"
    calendar += "END:VCALENDAR"
    
    return calendar


if __name__ == "__main__":
    events = []
    events.extend(culteum.getEvents([]))
    events.extend(nachtwerk.getEvents([]))
    events.extend(schwimmbad.getEvents([]))
    
    events.sort(key=lambda a: a[0])
    
    calendar = generateVCalendar(events)
    with open("gothcal.ics", "wb") as f:
        f.write(calendar.encode("utf-8"))