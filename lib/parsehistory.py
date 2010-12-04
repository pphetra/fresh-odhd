import urllib
import re
from tableparser import TableParser

import deflation

PRODUCT_MAP= {
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
    code = PRODUCT_MAP[type]
    url = 'http://203.148.172.199/pricestat/report2.asp?mode=A&product=%s' % (code,)
    f = urllib.urlopen(url)
    parser = MyParser()
    parser.feed(f.read().decode('tis-620'))
    return parser.rows

def build_row(product, year, row):
    ret_row = []
    for i in range(13):
        try:
            if len(str(i+1)) == 1:
                month = '0' + str(i+1)
            else:
                month = str(i+1)

            _key = str(year) + '/' + month
            _yearmonth = month + '/01/' + str(year)
            _deflation = deflation.deflate_map[_key]
            _row = [product, _yearmonth, str(row[i]), str(_deflation)]
            ret_row.append(_row)
        except:
            pass
    return ret_row

def build_data(product, rows):
    #data = [
    #    ['EGG3', '2010/01', 1.65, -0.1],
    #    ['EGG3', '2010/02', 1.50, 8],
    #]
    data = []
    for i, row in enumerate(rows):
        # Row no.1 is a table's header.
        if i != 0:
            year = row.pop(0)
            row.pop(len(row) - 1)
            for _row in build_row(product, year, row):
                data.append(_row)
    return data

def export_csv(rows):
    try:
        import csv
        w = csv.writer(open('fresh_odhd.csv', 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            w.writerow(row)
    except:
        pass


if __name__ == '__main__':
    data = []
    for product in PRODUCT_MAP.iterkeys():
        rows = parse(product)
        for _row in build_data(product, rows):
            data.append(_row) 
    export_csv(data)
