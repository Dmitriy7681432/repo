import requests
import pandas as pd

number_of_pages =1

job_tittle = ["'Data Analyst' and 'data scientist'"]
for job in job_tittle:
    data =[]
    for i in range(number_of_pages):
        url = 'https://api.hh.ru/vacancies'
        par = {'text': job, 'area':113, 'per_page':'10','page':i}
        r =requests.get(url,params=par)
        e= r.json()
        data.append(e)
        vacancy_details= data[0]['items'][0].keys()
        df = pd.DataFrame(columns =list(vacancy_details))
        ind = 0
        for i in range(len(data)):
            for j in range(len(data[i]['items'])):
                df.loc[ind] = data[i]['items'][j]
                ind+=1
    csv_name = job +'.csv'
    df.to_csv(csv_name)
# print(vacancy_details)
print(e)
# print(df)
# df =pd.read_csv("'Data Analyst' and 'data scientist'.csv")
# print(df.head())