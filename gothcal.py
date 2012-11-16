#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import culteum, nachtwerk, schwimmbad
import hashlib
from datetime import timedelta

def generateVCalendar(event_list):
    calendar =  u"BEGIN:VCALENDAR\r\n"
    calendar += u"PRODID:-//K Desktop Environment//NONSGML KOrganizer 4.4.5//EN\r\n"
    calendar += u"VERSION:2.0\r\n"
    calendar += u"CALSCALE:GREGORIAN\r\n"
    
    calendar += u"BEGIN:VTIMEZONE\r\n"
    calendar += u"TZID:Europe/Berlin\r\n"
    calendar += u"END:VTIMEZONE\r\n"
    
    for date, url, name, description, club in event_list:
        id = 0
        print(name,date)
        dtstart = date.strftime('%Y%m%d')
        dtend = (date+timedelta(1)).strftime('%Y%m%d')
        
        calendar += u"BEGIN:VEVENT\r\n"
        calendar += u"UID:{0}{1}@gothcal.dynamic-noise.net\r\n".format(hashlib.md5(name.encode('utf-8')).hexdigest(), dtstart)
        calendar += u"SUMMARY:"+name+u"\r\n"
        
        #calendar += u"DESCRIPTION:"
        #calendar += unicode(description)+u"\\n\\n"
        #calendar += u"\r\n"
        
        calendar += u"DTSTART;VALUE=DATE:"+dtstart+u"\r\n"
        calendar += u"DTEND;VALUE=DATE:"+dtend+u"\r\n"
        calendar += u"URL:"+url+u"\r\n"
        calendar += u"LOCATION:"+club+"\r\n"
        calendar += u"STATUS:CONFIRMED\r\n"
        calendar += u"TRANSP:OPAQUE\r\n"
        
        calendar += u"END:VEVENT\r\n"
    calendar += u"END:VCALENDAR"
    
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