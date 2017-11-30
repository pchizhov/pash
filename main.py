from itertools import count
from urllib import response
from pprint import pprint as pp
import requests
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime

ownId = 52972873
access_token = '026a76a2026a76a2026a76a28d0235b5520026a026a76a25876151a33205c78b6f08922'
domain = "https://api.vk.com/method"


def get_friends(user_id, fields):  # Список дат
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        "domain": domain,
        "access_token": access_token,
        "user_id": user_id,
        "fields": fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    friends_ids = []  # Выводит даты рождения друзей
    for n in range(response.json()['response']['count']):
        if response.json()['response']['items'][n].get(fields) != None:
            friends_ids.append(response.json()['response']['items'][n][fields])
    print(friends_ids)
    data = []  # Выводит даты рождения в которых есть число, месяц, год
    for k in range(len(friends_ids)):
        if len(friends_ids[k]) >= 8:
            data.append(friends_ids[k])
    return data
    return get_friends(ownId, 'bdate')


def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    data_1 = get_friends(ownId, 'bdate')
    print(data_1)
    year = []
    for i in range(len(data_1)):
        year.append((str(data_1[i]).split('.'))[2])
    age = []
    for i in range(len(year)):
        age.append(2017 - int(year[i]))  # возраст друзей
    age_user = int(sum(age) / len(age))  # возраст пользователя
    return age_user


print(age_predict(ownId))


def messages_get_history(user_id=ownId, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        "domain": domain,
        "access_token": access_token,
        "user_id": user_id,
        "offset": offset,
        "count": count
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    return response.json()  # Получаю сообщения с указанным пользователем


def count_dates_from_messages():
    history = messages_get_history(ownId)
    dates = []  # Получаю список дат
    count = history['response']['count']
    if count > 200:
        count = 200
    for n in range(count):
        message = history['response']['items'][n]
        date = datetime.fromtimestamp(message['date']).strftime("%Y-%m-%d")
        dates.append(date)

    from collections import Counter
    from operator import itemgetter

    data_count = Counter(dates)  # Получаю дату и сколько раз она повторяется
    data_count = list(data_count.items())
    data_count.sort(key=itemgetter(0))  # Сортирую от первой даты до последней
    key = []
    values = []
    for i in data_count:
        key.append((i[0]))
        values.append(i[1])
    return key, values  # Кортеж из списка дат и списка повторений

'''plotly.tools.set_credentials_file(username='kantegory', api_key='vm9txc36kh')
x = count_dates_from_messages()[0]
y = count_dates_from_messages()[1]
data = [go.Scatter(x=x, y=y)]
py.plot(data)
pp(count_dates_from_messages())
'''