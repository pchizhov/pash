from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session, fill
from bayes_ham_spam import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id).all()
    row[0].label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    fresh = get_news(n_pages=16)
    db = s.query(News).all()
    new = True
    for fresh_news in fresh:
        for db_news in db:
            if (fresh_news['title'], fresh_news['author']) ==\
               (db_news.title, db_news.author):
                new = False
                break
        if new:
            fill(fresh_news)
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
