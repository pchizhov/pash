import requests
import time
import plotly


config = {
    'VK_ACCESS_TOKEN': 'Tокен доступа для ВК',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly',
    'VK_USER_ID': 52972873,
    'DOMAIN': "https://api.vk.com/method"
}

plotly.tools.set_credentials_file(username=config['PLOTLY_USERNAME'], api_key=config['PLOTLY_API_KEY'])


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for n in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            content_type = response.headers.get('Content-Type')
            if not content_type == 'application/json; charset=utf-8':
                raise
            return response
        except requests.exceptions.RequestException:
            if n == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** n)
            time.sleep(backoff_value)


def get_friends(fields, user_id=config['VK_USER_ID']):
    """ Вернуть данные о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': config['DOMAIN'],
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    return response.json()


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    all_dates = [get_friends(user_id, 'bdate')['response']['items'][n]['bdate']
                   for n in range(get_friends(user_id, 'bdate')['response']['count'])
                   if get_friends(user_id, 'bdate')['response']['items'][n].get('bdate')]
    dates = [all_dates[i] for i in range(len(all_dates))
             if len(all_dates[i]) >= 8]
    ages = [2017 - int(i[-4:0]) for i in dates]
    avg_age = int(sum(ages) / len(ages))
    return avg_age


def messages_get_history(user_id=config['VK_USER_ID'], offset=0, count=20):
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'domain': config['DOMAIN'],
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'offset': offset,
        'count': count
    }

    query = '{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53'.format(**query_params)
    response = requests.get(query)
    return response.json()


def count_dates_from_messages(messages):
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    # PUT YOUR CODE HERE
    pass


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly
    :param freq_list: список дат и их частот
    """
    # PUT YOUR CODE HERE
    pass


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass


def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


x = count_dates_from_messages()[0]
y = count_dates_from_messages()[1]
data = [go.Scatter(x=x, y=y)]
py.plot(data)
pp(count_dates_from_messages())