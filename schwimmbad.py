# -*- coding: utf-8 -*-
"""
 Parser for Schwimmbad Club Heidelberg ( http://www.schwimmbad-club.de )

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

from html.parser import HTMLParser
import http.client
from datetime import datetime

class SchwimmbadParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.current_date = None
        self.get_date = False
        self.current_url = None
        self.output = []
    

    def handle_data(self, data):
        if self.get_date:
            self.get_date = False
            self.current_date = datetime.strptime(data, "%d.%m.%Y")
        elif self.current_date is not None and self.current_url is not None:
            if "schwarz" in data.lower():
                self.output.append((self.current_date, self.current_url, data, "", "Schwimmbad Club Heidelberg"))
                self.current_date = None
                self.current_url = None
    
    def handle_starttag(self, tag, attr):
        attr = dict(attr)
        if tag == "span" and "class" in attr and attr["class"] == "startpage-date":
            self.get_date = True
        elif tag == "a" and self.current_date is not None:
            self.current_url = attr["href"]
        
def getEvents(config):
    conn = http.client.HTTPConnection("www.schwimmbad-club.de")
    conn.request("GET", "/")
    resp = conn.getresponse()
    parser = SchwimmbadParser()
    parser.feed(str(resp.read()))
    conn.close()
    
    return parser.output

if __name__ == "__main__":
    print(getEvents([]))