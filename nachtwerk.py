# -*- coding: utf-8 -*-

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
    
    def handle_startendtag(self, tag, attr):
        if not self.in_program_block:
            return
        if tag == "hr":
            self.addDatasetIfNeccessary()
            self.new_block = True
            self.block_div_counter = 0
            self.current_dataset = []
        
    def handle_data(self, data):
        if self.get_data:
            self.current_dataset.append(data)
            self.get_data = False
    
    def handle_starttag(self, tag, attr):
        if tag == "h1":
            self.in_program_block = True
        elif self.in_program_block:
            attr = dict(attr)
            if tag == "div":
                self.div_depth += 1
            elif tag == "strong":
                self.get_data = True
            elif tag == "a":
                self.get_data = True
                url = attr["href"]
                if url[0] == "/":
                    url = "http://nachtwerk-musikclub.de"+url
                self.current_dataset.append(url)
    
    def handle_endtag(self, tag):
        if not self.in_program_block:
            return
        if tag == "div":
            self.div_depth -= 1
            if self.div_depth <= 0:
                self.in_program_block = False
                self.addDatasetIfNeccessary()
        
    def addDatasetIfNeccessary(self):
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
        if "partykingz" in lower_name:
            return
        elif "colo" in lower_name:
            return
        elif "rosapark" in lower_name:
            return
        elif "herz tanzt farben" in lower_name:
            return
        elif "da vibez" in lower_name:
            return
        elif "crazy friday" in lower_name:
            return
        elif "8090-party" in lower_name:
            return
        
        date = datetime.strptime(date.split(" ")[1], "%d.%m.%y")
        
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