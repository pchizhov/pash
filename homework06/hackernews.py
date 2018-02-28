from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session, fill
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id).one()
    row.label = label
    s.commit()
    if request.query.classify == 'True':
        redirect('/classify')
    else:
        redirect('/news')


@route("/update")
def update_news():
    recent_news = get_news()
    authors = [news['author'] for news in recent_news]
    titles = s.query(News.title).filter(News.author.in_(authors)).subquery()
    existing_news = s.query(News).filter(News.title.in_(titles)).all()
    for news in recent_news:
        if not existing_news or news not in existing_news:
            fill(news)
    redirect("/news")


@route("/classify")
def classify_news():
    recently_marked_news = s.query(News).filter(News.title not in x_train and News.label != None).all()
    x_extra_train = [row.title for row in recently_marked_news]
    y_extra_train = [row.label for row in recently_marked_news]
    classifier.fit(x_extra_train, y_extra_train)

    blank_rows = s.query(News).filter(News.label == None).all()
    x = [row.title for row in blank_rows]
    labels = classifier.predict(x)
    classified_news = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'good']
    return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier()
    marked_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in marked_news]
    y_train = [row.label for row in marked_news]
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
