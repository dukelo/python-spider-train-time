from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
import lxml
import requests

rideDate = datetime.now().strftime('%Y/%m/%d')
startTime = '06:00'
endTime = '23:59'

URL = 'https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime'
POST_URL = 'https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime'

response = requests.get(URL)

if response.status_code != 200:
    print('url error')

soup = BeautifulSoup(response.text, 'lxml')

key_place = [tag.getText() for tag in soup.select('#cityHot li button')]
value_place = [tag['title'] for tag in soup.select('#cityHot li button')]
dict_place = dict(zip(key_place, value_place))

csrf = soup.select('#pageContent > form > input')[0].get('value')
post_data = {
    'csrf': csrf,
    # 'startStation': dict_place[start_place],
    # 'endStation': dict_place[end_place],
    'startStation': '1000-臺北',
    'endStation': '4220-臺南',
    'transfer': 'ONE',
    'rideDate': rideDate,
    'startOrEndTime': 'true',
    'startTime': startTime,
    'endTime': endTime,
    'trainTypeList': 'ALL',
    'queryClassification': 'NORMAL',
    'query': '查詢'
}

response_post = requests.post(POST_URL, data=post_data)
if response_post.status_code != 200:
    print('url error')
soup = BeautifulSoup(response_post.text, 'lxml')
data = soup.select('#pageContent div.search-trip > table > tbody tr.trip-column')
results = []

# print(data[0].select('td')[0].select('li span.location')[1].getText().strip())

for i in range(len(data)):
    result = {
        '車種': data[i].select('td')[0].select('a')[0].getText(),
        '始發站': data[i].select('td')[0].select('li span.location')[0].getText().strip(),
        '終點站': data[i].select('td')[0].select('li span.location')[1].getText().strip(),
        '出發時間': data[i].select('td')[1].getText(),
        '抵達時間': data[i].select('td')[2].getText(),
        '行駛時間': data[i].select('td')[3].getText(),
        '經由': data[i].select('td')[4].getText(),
        '票價': data[i].select('td')[6].getText().strip()
    }

    results.append(result)

with open('train_time.txt', mode='w', encoding='utf-8') as file:
    for result in results:
        file.write(str(result)+'\n')
