# -*- coding: utf-8 -*-
import requests, json

url = "https://api.hh.ru/vacancies"


def fetch_hh_vacancies(url: str, page: int = 0):
    query_params = {
        'text': 'django OR fastapi OR aiohttp OR litestar OR flask',
        'per_page': 100,
        'page': page,
    }
    resp = requests.get(url, query_params)
    if resp.status_code != 200:
        print('Запрос не удался', resp.text)
    print(f"Успешно получены вакансии {page=}")
    result = resp.json()
    return result


def fetch_all_hh_vacancies(url: str):
    page = 0
    vacancies_data = []
    while True:
        if page == 20:
            break
        vacancies = fetch_hh_vacancies(url, page)
        if len(vacancies['items']) == 0:
            break
        vacancies_data.extend(vacancies['items'])
        page += 1
    print('norm')
    with open("vacansies.json", "w",encoding='utf-8') as file:
        file.write(json.dumps(vacancies_data, ensure_ascii=False))
    print('norm2')


def main():
    fetch_all_hh_vacancies(url)


if __name__ == "__main__":
    main()
# https://lk.pytex.school/teach/control/lesson/view/id/344830064