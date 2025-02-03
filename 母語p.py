import urllib.parse
import re
import requests
from bs4 import BeautifulSoup
session = requests.session()

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://inative2025.azurewebsites.net/game.asp',
    'Origin': 'https://inative2025.azurewebsites.net',
    'Host': 'inative2025.azurewebsites.net',
    'Content-Type': 'application/x-www-form-urlencoded',
    'cookies': ''  #你的cookie資料
}

data = {
    'zone': '區域',
    'sch_d': '學校級別',
    'sch_n': '學校',
    'degree': '年級',
    'degree_2': '班級',
    'degree_3': '',
    'num': '座號加姓名',
    'code': 'a', #語言代號例如閩南語為a(預設)
    'imageField.x': '92',
    'imageField.y': '52'
}

re_ = session.post(
    url='https://inative2025.azurewebsites.net/game.asp', headers=header, data=data)
html_content = re_.text
soup = BeautifulSoup(html_content, 'html.parser')
script_tags = soup.find_all('script')
for script in script_tags:
    if script.string and 'data: "value=' in script.string and '&tone=' in script.string:
        script_content = script.string
        break
value_match = re.search(r'data: "value=([^"]+)"', script_content)
tone_match = re.search(r'&tone=([a-f0-9]+)', script_content)
value_match = str(value_match.group(1))
tone_match = str(tone_match.group(1))


if value_match and tone_match:
    value = value_match
    tone = tone_match
else:
    print("未找到所需的資料")
original_string = value_match
encoded_string = urllib.parse.quote(original_string)

url = 'https://inative2025.azurewebsites.net/'
re_ = session.get(url=url+'outdata2.asp', data=f'value={value_match}')
data = f"sco=230&timestamp={encoded_string}&tone={tone_match}&tor={re_.text[-4:-1:1]}"

url = 'https://inative2025.azurewebsites.net/outdata.asp'
re_ = session.post(url=url, data=data, headers=header)
print(re_.text)
