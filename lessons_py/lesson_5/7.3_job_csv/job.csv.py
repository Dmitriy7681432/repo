import csv
#csv.writer
car_data = [['brand','price','year'],['Volvo',1.5,2017],['Lada',0.5,2018],['Audi',2.0,2019]]

with open('example.csv','w') as f:
    writer = csv.writer(f,delimiter = '&') # delimiter = '&'
    writer.writerows(car_data)

print('Writing complite!')

#csv.reader
with open('example.csv','r') as f:
    reader = csv.reader(f,delimiter = '&')
    for row in reader:
        print(row)

#csv.Dictwriter
data_dict = [{'Name': 'Dima', 'age':28},
            {'age':29, 'Name': 'Kate'},
            {'Name': 'Mike', 'age':31}]
field_names= ['Name','age']

with open('example_1.csv','w') as f:
    writer = csv.DictWriter(f,delimiter = '&',fieldnames=field_names)
    writer.writeheader()
    for i in range(len(data_dict)):
        writer.writerow((data_dict[i]))


#csv.Dictreader
with open('example_1.csv') as f:
    reader = csv.DictReader(f,delimiter = '&')
    for row in reader:
        print(row)

import pandas as pd

analize_csv = pd.read_csv('example_1.csv',sep='&')
print(type(analize_csv))
print(analize_csv)