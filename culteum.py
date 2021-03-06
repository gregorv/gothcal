# -*- coding: utf-8 -*-
"""
 Parser for Culteum Karlsruhe ( http://culteum.de )

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

import http.client
from html.parser import HTMLParser
from datetime import datetime

class CulteumParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.get_name = False
        self.get_date = False
        self.current_date = ""
        self.current_name = ""
        self.current_url = ""
        self.output = []
    

    def handle_data(self, data):
        if self.get_date:
            self.get_date = False
            if "-" in data:
                data = data.split("-")[0].replace("\\n", "").strip()
            self.current_date = datetime.strptime(data, "%d/%m/%Y")
            
            self.output.append((self.current_date, self.current_url, self.current_name, "", "Culteum Karlsruhe"))
    
    def handle_starttag(self, tag, attr):
        attr = dict(attr)
        if tag == "h2" and "class" in attr and attr["class"] == "entry-heading":
            self.get_name = True
        elif tag == "a" and self.get_name:
            self.current_url = attr["href"]
            self.current_name = attr["title"]
            self.get_name = False
        elif tag == "span" and "class" in attr and "meta-date" in attr["class"]:
             self.get_date = True
        
def getEvents(config):
    conn = http.client.HTTPConnection("culteum.de")
    conn.request("GET", "/events/events-default/")
    resp = conn.getresponse()
    parser = CulteumParser()
    parser.feed(resp.read().decode("utf-8", "ignore"))
    
    return parser.output

if __name__ == "__main__":
    print(getEvents([]))