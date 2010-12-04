from HTMLParser import HTMLParser
 
# Print debug info
markup_debug_low = not True
markup_debug_med = not True
 
# Generic HTML table parser
class TableParser(HTMLParser):
 
    def __init__(self):
        HTMLParser.__init__(self)
        self._td_cnt = 0
        self._tr_cnt = 0
        self._curr_tag = ''
 
    def handle_starttag(self, tag, attrs):
        self._curr_tag = tag
        if tag == 'td':
            self._td_cnt += 1
            self.col_start(self._td_cnt)
            if markup_debug_low: print "<TD> --- %s ---" % self._td_cnt
        elif tag == 'tr':
            self._td_cnt = 0
            self._tr_cnt += 1
            self.row_start(self._tr_cnt)
            if markup_debug_low: print "<TR> === %s ===" % self._tr_cnt
        else:
            if markup_debug_low: print "<%s>" % tag
 
    def handle_endtag(self, tag):
        if markup_debug_low: print "</%s>" % tag
        # it's possible to check "start tag - end tag" pair here (see, tag and self._curr_tag)
        if tag == 'tr':
            self.row_finish(self._tr_cnt)
        elif tag == 'td':
            self.col_finish(self._td_cnt)
        else:
            pass
 
    def handle_data(self, data):
        #if markup_debug_low: print u'[%s,%s] %s: "%s"' % (self._tr_cnt, self._td_cnt, self._curr_tag, unicode(data, 'mbcs'))
        self.process_raw_data(self._tr_cnt, self._td_cnt, self._curr_tag, data)
 
    # Overridable 
    def process_raw_data(self, row, col, tag, data):
        if row > 0 and col > 0:
            self.process_cell_data(row, col, tag, data)
        else:
            pass    # outside the table
 
    # Overridable 
    def process_cell_data(self, row, col, tag, data):
        pass
 
    # Overridable 
    def row_start(self, row):
        pass
 
    # Overridable 
    def row_finish(self, row):
        pass
 
    # Overridable 
    def col_start(self, col):
        pass
 
    # Overridable 
    def col_finish(self, col):
        pass
