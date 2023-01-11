import requests,csv
import pandas as pd
import seaborn as sns
import style

def pars_hh(vacancy,city):
    number_of_pages = 200
    # job_tittle = ["'Data Analyst' and 'data scientist'"]
    job_tittle = []
    job_tittle.append(vacancy)
    job_tittle_t = (''.join(job_tittle)).title()
    job_tittle_lower= job_tittle_t.lower()
    lst_rows = []
    lst_rows1 = []
    ls=[]
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
        # print(data[0]['items'])
        for i in data[0]['items']:
            # print(i.get('name'))
            if job in i.get('name') or job_tittle_t in i.get('name') or job_tittle_lower in i.get('name'):
                ind+=1
                lst_rows.append(ind)
                try:
                    name = i.get('name')
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
                    if salary_from == None: salary_from ="-"
                    lst_rows.append(salary_from)
                except AttributeError: salary_from ='-'; lst_rows.append(salary_from)
                try:
                    salary_to = i.get('salary').get('to')
                    if salary_to == None: salary_to ="-"
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
                # print(type(ind),type(name),type(adress_raw),type(adress_metro_station_name),
                #       type(employer_name),type(salary_from),type(salary_to),type(salary_currency),
                #       type(alternate_url))
                lst_rows1.append(lst_rows)
                # print(type(lst_rows[4]))

                lst_rows=[]

        pd.options.display.max_columns = 200
        pd.options.display.max_rows = 200
        pd.set_option('display.max_colwidth',None)
        pd.set_option('display.width',None)

        df =pd.DataFrame({
          '№ п.п.':[i[0] for i in lst_rows1],
          # '№ п.п.':[1,2,3,4]
          'Название вакансии':[i[1] for i in lst_rows1],
          'Адрес':[i[2] for i in lst_rows1],
          'Метро': [i[3] for i in lst_rows1],
          'Организация':[i[4] for i in lst_rows1],
          'Зарплат от':[i[5] for i in lst_rows1],
          'Зарплат до':[i[6] for i in lst_rows1],
          'Валюта':[i[7] for i in lst_rows1],
          'Ссылка':[i[8] for i in lst_rows1],
        })
        # df.reset_index(drop=True,inplace=True)
        # df = df.style.hide_index()
        df =df.to_string(index=False)
        # print(df)
        ls.append(df)

        lst_head = [['№ п.п.', 'Название вакансии','Адрес','Метро','Организация',
                     'Зарплата от','Зарплата до','Валюта','Ссылка']]
        # print(lst_rows1[1][0])


        #Запись в csv
        myFile = open('example2.csv', 'w', encoding='utf-32', newline='')
        with myFile:
            writer = csv.writer(myFile, delimiter='\t')
            writer.writerows(lst_head)
            writer.writerows(lst_rows1)

        # myFile1 = open('text.txt', 'w')
        # with myFile1:
        #     myFile1.write(str(ls))
        # ad = pd.read_csv('example2.csv',encoding='utf-32',sep='\t')
        # print(ad)
    # print(lst_rows1)
    # for i in lst_rows1:
    #     print(' '.join(map(str,i)))
    return lst_rows1

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
