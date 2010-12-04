import csv

rows = list(csv.reader(open('oil.csv', 'r')))
print "oil_map = {"
for row in rows[1:-1]:
    if (row[1]):
        x = row[0].split('/')
        tmp = "%s/%s" % ((int(x[2]) + 543), x[1])
        print "'%s': %s," % (tmp, row[1])
print "}"