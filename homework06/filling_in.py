from scrapper import get_news
from db import News, session


news_list = get_news('https://news.ycombinator.com/newest', n_pages=40)
for dictionary in news_list:
    s = session()
    news = News(title=dictionary['title'],
                author=dictionary['author'],
                url=dictionary['url'],
                comments=dictionary['comments'],
                points=dictionary['points'])
    s.add(news)
    s.commit()
