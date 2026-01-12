# -*- coding: utf-8 -*-
import requests, io, sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

main_page = "https://habr.com/ru/articles/top/daily/"

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


# User-Agent необходим чтобы при запросе на сайт, в заголовке было указано,
# что как будто запрос с браузера, а не с python кода
def get_url_html(url: str) -> str:
    res = requests.get(
        url,
        headers={
            "User-Agent": UserAgent().google,
        }
    )
    return res.text


def get_soup(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, features='lxml')


def get_all_habr_posts(soup: BeautifulSoup):
    all_arcticles_soup = soup.find_all("a", class_='tm-title__link')
    for article_soup in all_arcticles_soup:
        article_title: str = article_soup.find('span').text
        print(f"{article_title=}")
        rating = article_soup.find('span',class_='tm-icon-counter__value')
        print(f"{rating=}")



def main():
    html = get_url_html(main_page)
    soup = get_soup(html)
    get_all_habr_posts(soup)


if __name__ == "__main__":
    main()
