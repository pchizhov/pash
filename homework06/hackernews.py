from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session, fill
from bayes import NaiveBayesClassifier


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
    if request.query.classify == 'True':
        redirect('/classify')
    else:
        redirect('/news')


@route("/update")
def update_news():
    s = session()
    fresh = get_news()
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
    s = session()
    classifier = NaiveBayesClassifier()
    train = s.query(News).filter(News.label != None).all()
    x_train, y_train = [], []
    for row in train:
        x_train.append(row.title)
        y_train.append(row.label)
    classifier.fit(x_train, y_train)

    to_do = s.query(News).filter(News.label == None).all()
    x_to_do = [row.title for row in to_do]
    labels = classifier.predict(x_to_do)
    classified_news = [to_do[i] for i in range(len(to_do)) if labels[i] == 'good']
    return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
