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
            {'Name': 'Kate', 'age':29},
            {'Name': 'Mike', 'age':31}]
field_names= ['Name','age']


