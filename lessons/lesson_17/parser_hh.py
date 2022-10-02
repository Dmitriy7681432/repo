import requests,csv
import pandas as pd
def pars_hh(vacancy,city):
    number_of_pages = 1
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
            par = {'text': job, 'area':city_loc, 'per_page':'4','page':i}
            r =requests.get(url,params=par)
            e= r.json()
            data.append(e)
        # print(data[0]['items'])
        for i in data[0]['items']:
            # print(i.get('name'))
            if job in i.get('name') or job_tittle_t in i.get('name') or job_tittle_lower in i.get('name'):
                ind+=1
                lst_rows.append(ind)
                try:
                    name = i.get('name')
                    print(type(name))
                    lst_rows.append(name)
                except AttributeError: name ='-'; lst_rows.append(name)
                try:
                    adress_raw = i.get('address').get('raw')
                    lst_rows.append(adress_raw)
                except AttributeError: adress_raw ='-'; lst_rows.append(adress_raw)
                try:
                    adress_metro_station_name = i.get('address').get('metro').get('station_name')
                    lst_rows.append(adress_metro_station_name)
                except AttributeError: adress_metro_station_name='-'; lst_rows.append(adress_metro_station_name)
                try:
                    employer_name = i.get('employer').get('name')
                    lst_rows.append(employer_name)
                except AttributeError: employer_name ='-'; lst_rows.append(employer_name)
                try:
                    salary_from = i.get('salary').get('from')
                    lst_rows.append(salary_from)
                except AttributeError: salary_from ='-'; lst_rows.append(salary_from)
                try:
                    salary_to = i.get('salary').get('to')
                    lst_rows.append(salary_to)
                except AttributeError: salary_to ='-'; lst_rows.append(salary_to)
                try:
                    salary_currency = i.get('salary').get('currency')
                    lst_rows.append(salary_currency)
                except AttributeError: salary_currency ='-'; lst_rows.append(salary_currency)
                try:
                    alternate_url = i.get('alternate_url')
                    lst_rows.append(alternate_url)
                except AttributeError: alternate_url ='-'; lst_rows.append(alternate_url)

                lst_rows1.append(lst_rows)
                lst_rows=[]
        # print(lst_rows1)
                df =pd.DataFrame({
                  '№ п.п.':ind,
                  'Название вакансии':name,
                  'Адерс': adress_raw,
                  'Метро': adress_metro_station_name,
                  'Организация':employer_name,
                  'Зарплат от':salary_from,
                  'Зарплат до':salary_to,
                  'Валюта':salary_currency,
                  'Ссылка':alternate_url
                })
                print(df)


        lst_head = [['№ п.п.', 'Название вакансии','Адрес','Метро','Организация',
                     'Зарплата от','Зарплата до','Валюта','Ссылка']]



        #Запись в csv
        myFile = open('example2.csv', 'w', encoding='utf-32', newline='')
        with myFile:
            writer = csv.writer(myFile, delimiter='\t')
            writer.writerows(lst_head)
            writer.writerows(lst_rows1)

            # vacancy_details= data[0]['items'][0].keys()
            # print(type(vacancy_details))
            # df = pd.DataFrame(columns =list(vacancy_details))
            # print(df)
            # ind = 0
            # for i in range(len(data)):
            #     for j in range(len(data[i]['items'])):
            #         df.loc[ind] = data[i]['items'][j]
            #         ind+=1
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
            return i.get('id')
        else:
            for i in ac:
                if i.get('name') == city:
                    return i.get('id')

if __name__ == '__main__':
    pars_hh('Java','Москва')
    # pars_city('Московская область')
