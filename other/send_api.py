import requests
import json
from datetime import datetime

params = {
    "identify": "staff",
    "ST_NAME" : '李主翔',
    "ST_NUMBER" : '7108056070',
    "ST_CALICENSE": 'sip347',
    "ST_EMAIL" : 'jeffzhux@gmail.com',
    "ST_USERNAME" : 'jeffzhux',
    "ST_PASSWORD" : 'jeffzhux',
}
url = 'http://127.0.0.1:8080/app/register.html'
html = requests.post(f'{url}', json.dumps(params)) # select

# print(json.dumps(params))
# print(url)
# html = requests.post(f'{url}', json.dumps(params)) # insert

# url = 'http://127.0.0.1:8000/appapi/get_PARKING_SPACES_info_by_PS_CODE'
# html = requests.get(f'{url}/A0003') # select

# params = {
#     "PA_PLID" : 'PL_00001',
#     "PA_PSID" : 'PS_823f3f63a6c311edba854201c0a80002',
#     "PA_LICENSE": 'PR6548',
#     "PA_IMAGE" : '/Entry_image/A_0090_time.jpg',
# }
# url = 'http://127.0.0.1:8000/webapi/insert_park'
# print(json.dumps(params))
# html = requests.post(f'{url}', json.dumps(params)) # select


# url = 'http://10.0.0.2:8000/webapi/insert_parking_space'
# html = requests.post(f'{url}') # select

# print(html.text)
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# print(pwd_context.hash('password'))