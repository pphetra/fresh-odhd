from lxml import etree
import copy
from operator import itemgetter, attrgetter

THRESHOLD = 12
LINE_THRESHOLD = 7
MIN_THRESHOLD = 2

SPECIAL_MAP = {
    '(': 1,
    '.': 1
}

class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""
    def __init__(self, default, **items):
        dict.__init__(self, **items)
        self.default = default

    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        else:
            ## Need copy in case self.default is something like []
            return self.setdefault(key, copy.deepcopy(self.default))

    def __copy__(self):
        return DefaultDict(self.default, **self)
        
        

def parsestyle(text):
    elms = text.split(';')
    ret = {}
    for tmp in elms:
        pair = tmp.split(':')
        if len(pair) > 1:
            ret[pair[0].strip()] = pair[1].strip()
    return ret
    
def px2int(text):
    return int(text.replace('px', ''))
    
def groupline(lines):
    keys = sorted(lines.keys())
    linemap = DefaultDict([])
    curkey = -1
    for key in keys:
        if curkey > -1:
            if (key - curkey) > LINE_THRESHOLD:
                curkey = key
        else:
            curkey = key
        
        linemap[curkey] += lines[key]
        
    return linemap
    
def grouphorizontal(elms):
    buffer = ''
    lastpos = -1
    curgroup = ''
    groups = []
    for pos,elm in elms:
        if lastpos != -1:
            if pos - lastpos > THRESHOLD:
                groups.append(curgroup)
                curgroup = elm
            else:
                curgroup += elm
        else:
            curgroup = elm
            
        lastpos = pos
        
    groups.append(curgroup)
    return groups
    
def sortedDictValues(adict):
    keys = adict.keys()
    keys.sort()
    return [adict[key] for key in keys]
    
def sortThai(ary):
    newary = sorted(ary, key=itemgetter(0))
    finalary = []
    curpos = -1
    for pos,ch in newary:
        if curpos > -1:
            if (pos - curpos > MIN_THRESHOLD):
                curpos = pos
        else:
            curpos = pos
        finalary.append((curpos, ch))
                            
    def thaicompare(left, right):
        if left[0] == right[0]:
            if right[1] in SPECIAL_MAP:
                return SPECIAL_MAP[right[1]]
            else:
                return cmp( right[1], left[1])
        else:
            return cmp(left[0], right[0])
    return sorted(finalary, cmp=thaicompare)

def parse(file):
    parser = etree.HTMLParser()
    tree = etree.parse(file, parser)
    
    context = etree.iterwalk(tree.getroot(), events=('end',), tag='span')
    lines = DefaultDict([])
    for action,elm in context:
        ch = elm.text
        if ch:
            style = parsestyle(elm.attrib['style'])
            top = px2int(style['top'])
            left = px2int(style['left'])
            lines[top].append((left, ch))

    lines = groupline(lines)
    
    finalLines = {}
    for pos,ary in lines.items():
        tmp = sortThai(ary)
        finalLines[pos] = grouphorizontal(tmp)
        
    return sortedDictValues(finalLines)
        
        

if __name__ == '__main__':
    f = file('/tmp/x.html', 'r')
    lines = parse(f)
    for line in lines:
        for g in line:
            print ''.join(g)
        print '-------\n'