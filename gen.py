import csv

rows = list(csv.reader(open('index_cfi.csv', 'r')))
print "deflate_map = {"
for row in rows[1:-1]:
    if (row[1]):
        print "'%s': %s," % (row[0], row[1])
print "}"