from datetime import datetime, timedelta
import requests
import time
import pandas as pd

def get_posts_from_vkapi(start_datetime, end_datetime, topic):
    '''
    Извлечь данные о пользовательских публикациях с помощью VK API
    
    Parameters
    ----------
    start_datetime : datetime.datetime
        Дата старта периода, за который собираются данные
    end_datetime : datetime.datetime
        Дата окончания периода, за который собираются данные
    topic : string
        Тема, упоминающаяся в публикациях
    '''
    assert isinstance(start_datetime, datetime), 'Неверный формат данных'
    assert isinstance(end_datetime, datetime), 'Неверный формат данных'

    ACCESS_TOKEN = 'YOUR TOKEN'
    VK_API = 'https://api.vk.com/method/newsfeed.search'
    VK_API_VERSION = '5.199'

    delta = timedelta(hours=1)
    tmp_start_datetime = start_datetime
    tmp_end_datetime = tmp_start_datetime + delta

    result = []
    
    # цикл по времени
    while tmp_end_datetime <= end_datetime:
        # print(f'Период: {tmp_start_datetime} - {tmp_end_datetime}')
        parameters = {
            "access_token": ACCESS_TOKEN,
            'count': 200,
            "q": topic,
            "v": VK_API_VERSION,
            "start_time": tmp_start_datetime.timestamp(),
            "end_time": tmp_end_datetime.timestamp()
        }
        # вызов метода API
        response = requests.get(VK_API, parameters)
        
        if 'error' in response.json():
            print('Неудачный запрос по API')
            return None
        else: 
            items = response.json()['response']['items']
            result += items
        
        tmp_start_datetime = tmp_end_datetime
        tmp_end_datetime += delta

        # чтобы не было connection broken
        time.sleep(0.2)
    
    return result

def parse_vk_posts_info(data):
    '''
    Извлечь из выгруженных данных ценную информацию
    
    Parameters
    ----------
    data : list
        Массив словарей, которые содержат данные о публикациях
    '''
    result = {
        "id": [],
        "from_id": [],
        "date": [],
        "text": [],
        "likes": [],
        "views": [],
        "reposts": [],
        "comments": [],               
    }
    for record in data:
        if record['post_type'] == 'post':
            result['id'].append(record['id'])
            result['date'].append(datetime.fromtimestamp(record['date']).strftime('%Y-%m-%d'))
            result['from_id'].append(record['from_id'])
            result['text'].append(record['text'])
            result['likes'].append(record.get('likes', {'count': 0})['count'])
            result['views'].append(record.get('views', {'count': 0})['count'])
            result['reposts'].append(record.get('reposts', {'count': 0})['count'])
            result['comments'].append(record.get('comments', {'count': 0})['count'])
        else:
            continue

    return pd.DataFrame(result)