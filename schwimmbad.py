# -*- coding: utf-8 -*-

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