# -*- coding: utf-8 -*-
import requests, io, sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint

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


@dataclass
class ArticleData:
    title: str
    views: str
    url: str

    def __repr__(self):
        return f'{__class__.__name__}. Title: {self.title}, Views: {self.views}, URL: {self.url}'


def get_all_habr_posts(soup: BeautifulSoup) -> list[ArticleData]:
    posts_data = []
    all_arcticles_soup = soup.find_all("article", class_='tm-articles-list__item')
    for article_soup in all_arcticles_soup:
        article_title: str = article_soup.find('a', class_="tm-title__link").find('span').text
        article_views: str = article_soup.find('span', class_='tm-icon-counter__value').text
        article_url: str = article_soup.find('a').get('href')
        posts_data.append(ArticleData(
           title=article_title,
           views=article_views,
           url=article_url
        ))
    return posts_data


def main():
    html = get_url_html(main_page)
    soup = get_soup(html)
    posts = get_all_habr_posts(soup)
    pprint(posts)
    # print(f"{posts=}")


if __name__ == "__main__":
    main()
