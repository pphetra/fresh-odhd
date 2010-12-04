import urllib
import re
from tableparser import TableParser

OBJECT_MAP= {
    'PORK_SAPOK': '941',
    'EGG3': '231',
    'CHICKEN': '151',
    'PLATOO': '1065',
    'KANA': '640'
}

class MyParser(TableParser):
    def __init__(self):
        TableParser.__init__(self)
        self.rows = []

    # Overridable 
    def process_cell_data(self, row, col, tag, data):
        if not re.match('\s+', data):
            if tag == 'td':
                self.cur_row.append(data)
        
    # Overridable 
    def row_start(self, row):
        self.cur_row = []

    # Overridable 
    def row_finish(self, row):
        self.rows.append(self.cur_row)

    # Overridable 
    def col_start(self, col):
        pass

    # Overridable 
    def col_finish(self, col):
        pass

def parse(type):
    code = OBJECT_MAP[type]
    url = 'http://203.148.172.199/pricestat/report2.asp?mode=A&product=%s' % (code,)
    f = urllib.urlopen(url)
    parser = MyParser()
    result = parser.feed(f.read().decode('tis-620'))
    return result
        
if __name__ == '__main__':
    url = 'http://203.148.172.199/pricestat/report2.asp?mode=A&product=231'
    f = urllib.urlopen(url)
    parser = MyParser()
    result = parser.feed(f.read().decode('tis-620'))
    for row in parser.rows:
        print row
