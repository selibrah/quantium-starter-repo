import csv
from numpy import asarray, save,load
from numpy import savetxt


productsInfo = []


def getPrice(string):
    return float(string.replace('$', ''))

with open('daily_sales_data_0.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[0] != 'pink morsel': 
            continue
        sales = getPrice(row[1]) * int(row[2])
        obj = {
                'Date': row[3],
                'Sales': sales,
                'Region': row[4]
                }
        productsInfo.append(obj)
        line_count += 1

data = asarray(productsInfo)
save('result.npy',data)


