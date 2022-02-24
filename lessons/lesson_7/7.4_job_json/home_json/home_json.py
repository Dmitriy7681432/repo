import json

with open('car.txt') as f:
    car_rand = []
    for row in f:
        car_rand.append(row.split())
print(row.split())
print(car_rand)
print(car_rand[0])

with open('car1.txt','w') as f:
    json.dump(str(car_rand[0]),f)