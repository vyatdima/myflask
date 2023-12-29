from bs4 import BeautifulSoup
import requests

url = 'http://greatwalk.ru/events/'
url = 'https://toplist.run/feed'
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")
# allEvent = soup.findAll('div', class_='col-lg-3 col-md-4 mb-2')
# for data in allEvent:
#     df_img = data.find('img', class_='card-img-top')
#     name_img = df_img.get('src')
#     print(name_img)

allEvent = soup.findAll('div', id_='app')
print(allEvent)
