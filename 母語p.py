import urllib.parse
import re
import requests
from bs4 import BeautifulSoup
# 手動解析 cookies
session = requests.session()
# with open('cookies.txt', 'r', encoding='utf-8') as f:
#     cookies = {}
#     for line in f:
#         if not line.startswith('#') and line.strip():
#             parts = line.strip().split('\t')
#             if len(parts) > 6:
#                 cookies[parts[5]] = parts[6]
# session.cookies.update(cookies)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://inative2025.azurewebsites.net/game.asp',
    'Origin': 'https://inative2025.azurewebsites.net',
    'Host': 'inative2025.azurewebsites.net',
    'Content-Type': 'application/x-www-form-urlencoded',
    'cookies': '_gid=GA1.3.1406388514.1738482175; ASPSESSIONIDAECCTDRC=INJFPIBAHHFKOKFCNJOHMKMK; ARRAffinity=50e6c634681468f1d8b9d97d7a947b20db7c13c796609faa97fdd181ace77dff; ARRAffinitySameSite=50e6c634681468f1d8b9d97d7a947b20db7c13c796609faa97fdd181ace77dff; _gat_gtag_UA_132743848_1=1; _ga_E5YBGXR7XX=GS1.1.1738567030.3.1.1738567883.60.0.0; _ga=GA1.1.1491043906.1738482175'
}

data = {
    'zone': '中正區',
    'sch_d': '高中',
    'sch_n': '市立成功高中',
    'degree': '2',
    'degree_2': '10',
    'degree_3': '',
    'num': '23辜名緯',
    'code': 'a',
    'imageField.x': '92',
    'imageField.y': '52'
}

re_ = session.post(
    url='https://inative2025.azurewebsites.net/game.asp', headers=header, data=data)
# print(re_.text)
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(re_.text)
with open('test.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找包含所需資料的 <script> 標籤
script_tags = soup.find_all('script')

# 遍歷所有 <script> 標籤，查找所需的資料
for script in script_tags:
    if script.string and 'data: "value=' in script.string and '&tone=' in script.string:
        script_content = script.string
        break

# 提取所需的資料

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
