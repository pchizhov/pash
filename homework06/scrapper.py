import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news_table = parser.table.findAll('table')[1]
    all_rows = news_table.findAll('tr')[:90]
    news_rows = [[all_rows[i], all_rows[i+1]] for i in range(90) if i % 3 == 0]
    for news in news_rows:
        first_td = news[0].findAll('td')[2]
        second_td = news[1].findAll('td')[1]

        str_comments = second_td.findAll('a')[-1].text
        if str_comments == 'discuss':
            comments = 0
        else:
            comments = int(str_comments[0])

        points = int(second_td.span.text[0])

        link = str(first_td.a)[27:]
        href_end = link.find('"')
        href = link[:href_end]
        if 'http' not in href:
            url = 'https://news.ycombinator.com/' + href
        else:
            url = href

        news_dict = {'author': second_td.a.text,
                     'comments': comments,
                     'points': points,
                     'title': str(first_td.a.text),
                     'url': url
                     }

        news_list.append(news_dict)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    news_table = parser.table.findAll('table')[1]
    final_row = news_table.findAll('tr')[91]
    link = str(final_row.findAll('td')[1].a)
    url_start = link.find('newest')
    url_end = link.find('" rel=')
    next_page_code = link[url_start:url_end]
    return next_page_code


def get_news(url='https://news.ycombinator.com/newest', n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(2)
    return news
