import requests,csv
import pandas as pd
def pars_hh(vacancy,city):
    number_of_pages = 200
    # job_tittle = ["'Data Analyst' and 'data scientist'"]
    job_tittle = []
    job_tittle.append(vacancy)
    job_tittle_t = (''.join(job_tittle)).title()
    job_tittle_lower= job_tittle_t.lower()
    lst_rows = []
    lst_rows1 = []
    ind =0
    city_loc =int(pars_city(city))
    for job in job_tittle:
        data =[]
        for i in range(number_of_pages):
            url = 'https://api.hh.ru/vacancies'
            par = {'text': job, 'area':city_loc, 'per_page':'100','page':i}
            r =requests.get(url,params=par)
            e= r.json()
            data.append(e)
            # print(data)
            # print(data[0]['items'])
            # print('\n')
        # print(data[0]['items'])
        for i in data[0]['items']:
            print(i.get('name'))
            # if i.get('name')==job or i.get('name') ==job_tittle_t:
            if job in i.get('name') or job_tittle_t in i.get('name') or job_tittle_lower in i.get('name'):
                ind+=1
                lst_rows.append(ind)
                try:
                    name = i.get('name')
                    lst_rows.append(name)
                except AttributeError: lst_rows.append('-')
                try:
                    adress_raw = i.get('address').get('raw')
                    lst_rows.append(adress_raw)
                except AttributeError: lst_rows.append('-')
                try:
                    adress_metro_station_name = i.get('address').get('metro').get('station_name')
                    lst_rows.append(adress_metro_station_name)
                except AttributeError: lst_rows.append('-')
                try:
                    employer_name = i.get('employer').get('name')
                    lst_rows.append(employer_name)
                except AttributeError: lst_rows.append('-')
                try:
                    salary_from = i.get('salary').get('from')
                    lst_rows.append(salary_from)
                except AttributeError: lst_rows.append('-')
                try:
                    salary_to = i.get('salary').get('to')
                    lst_rows.append(salary_to)
                except AttributeError: lst_rows.append('-')
                try:
                    salary_currency = i.get('salary').get('currency')
                    lst_rows.append(salary_currency)
                except AttributeError: lst_rows.append('-')
                try:
                    alternate_url = i.get('alternate_url')
                    lst_rows.append(alternate_url)
                except AttributeError: lst_rows.append('-')

                lst_rows1.append(lst_rows)
                lst_rows=[]
                # print(lst_rows)
        print(lst_rows1)

        lst_head = [['№ п.п.', 'Название вакансии','Адрес','Метро','Организация','Зарплата от','Зарплата до','Валюта','Ссылка']]
        #Запись в csv
        myFile = open('example2.csv', 'w', encoding='utf-32', newline='')
        with myFile:
            writer = csv.writer(myFile, delimiter='\t')
            writer.writerows(lst_head)
            writer.writerows(lst_rows1)
    #     vacancy_details= data[0]['items'][0].keys()
        #     df = pd.DataFrame(columns =list(vacancy_details))
        #     ind = 0
        #     for i in range(len(data)):
        #         for j in range(len(data[i]['items'])):
        #             df.loc[ind] = data[i]['items'][j]
        #             ind+=1
        # csv_name = job +'.csv'
        # df.to_csv(csv_name,encoding='utf-32')
def pars_city(city):
    data =[]
    url = 'https://api.hh.ru/areas/113'
    r =requests.get(url)
    e= r.json()
    data.append(e)
    for i in data[0]['areas']:
        ac=i.get('areas')
        if i.get('name') == city:
            # print('Республика',i.get('id'))
            return i.get('id')
        else:
            for i in ac:
                if i.get('name') == city:
                    # print('Город',i.get('id'))
                    return i.get('id')

if __name__ == '__main__':
    pars_hh('Python','Москва')
    # pars_city('Московская область')
