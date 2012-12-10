# -*- coding: utf-8 -*-
"""
 Parser for Nachtwerk Musikclub Karlsruhe ( http://nachtwerk-musikclub.de )

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

class NachtwerkParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.div_depth = 0
        self.block_div_counter = 0
        self.new_block = False
        self.in_program_block = False
        self.get_data = False
        self.output = []
        self.current_dataset = []
        self.cur_data_tag = ""
        self.prev_data_tag = ""
    
    def handle_startendtag(self, tag, attr):
        if not self.in_program_block:
            return
        if tag == "hr":
            self.addDatasetIfNeccessary()
            self.new_block = True
            self.block_div_counter = 1
            self.current_dataset = []
        
    def handle_data(self, data):
        if self.get_data:
            print(self.cur_data_tag)
            if self.cur_data_tag == self.prev_data_tag \
                and self.cur_data_tag == "strong" \
                and len(self.current_dataset) > 0:
                try:
                    datetime.strptime(self.current_dataset[-1].split(" ")[1], "%d.%m.%y")
                    self.current_dataset.append(data)
                except Exception as e:
                    print(e,data)
                    self.current_dataset[-1] += data
            else:
                self.current_dataset.append(data)
            self.get_data = False
            print(repr(self.current_dataset[-1]))
            self.prev_data_tag = self.cur_data_tag
    
    def handle_starttag(self, tag, attr):
        if not self.in_program_block and tag == "div":
            attr = dict(attr)
            if "class" in attr and attr["class"] == "article":
                self.in_program_block = True
        elif self.in_program_block:
            attr = dict(attr)
            if tag == "div":
                self.div_depth += 1
            elif tag == "strong" and not self.get_data:
                self.get_data = True
                self.cur_data_tag = tag
            elif tag == "a":
                self.get_data = True
                self.cur_data_tag = tag
                url = attr["href"]
                if url[0] == "/":
                    url = "http://nachtwerk-musikclub.de"+url
                self.current_dataset.append(url)
                
    
    def handle_endtag(self, tag):
        if not self.in_program_block:
            return
        if tag == "div":
            self.div_depth -= 1
            print(self.div_depth)
            if self.div_depth < 0:
                self.in_program_block = False
                self.addDatasetIfNeccessary()
        
    def addDatasetIfNeccessary(self):
        print("addDatasetIfNeccessary", not not self.current_dataset)
        if not self.current_dataset:
            return
        
        try:
            if len(self.current_dataset) == 2:
                date, name = self.current_dataset[0:2]
                link = ""
            else:
                date, link, name = self.current_dataset[0:3]
        except ValueError:
            return
        lower_name = name.lower()
        blacklist = ["partykingz", "colo", "rosapark", "herz tanzt farben",
            "da vibez", "crazy friday", "8090-party", "geschlossen"]
        for party in blacklist:
            if party in lower_name:
                return
        
        try:
            date = datetime.strptime(date.split(" ")[1], "%d.%m.%y")
        except ValueError:
            date = datetime.strptime(date.split(" ")[1], "%d.%m.%Y")
        
        self.output.append((date, link, name, "", "Nachtwerk Karlsruhe"))
        
def getEvents(config):
    conn = http.client.HTTPConnection("www.nachtwerk-musikclub.de")
    conn.request("GET", "/")
    resp = conn.getresponse()
    parser = NachtwerkParser()
    parser.feed(str(resp.read()))
    conn.close()
    
    return parser.output

if __name__ == "__main__":
    print(getEvents([]))