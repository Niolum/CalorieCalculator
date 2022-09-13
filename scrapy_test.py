from bs4 import BeautifulSoup
import requests


url = 'https://supercalorizator.ru/#'

page = requests.get(url)

categories_image = []
categories_name = []

if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)

    all_categories = soup.findAll('div', class_='main_block')
    # print(all_categories)
    for data in all_categories:
        if data.find('div', class_='menu_name'):
            data = data.text.replace('\n', '')
            categories_name.append(data)

    for data in all_categories:
        if data.find('div', class_='main_menu_image'):
            # img_url = data.text
            # categories_image.append(img_url)
            img = data.find('img')
            img_url = img.attrs.get('src')
            img_url = 'https://supercalorizator.ru/' + img_url
            categories_image.append(img_url)  
    
    all_cat_divi = soup.findAll('divi', class_='main_block')
# print(all_categories)
    for data in all_cat_divi:
        if data.find('div', class_='menu_name'):
            data = data.text.replace('\n', '')
            categories_name.append(data)

    for data in all_cat_divi:
        if data.find('div', class_='main_menu_image'):
                # img_url = data.text
                # categories_image.append(img_url)
                img = data.find('img')
                img_url = img.attrs.get('src')
                img_url = 'https://supercalorizator.ru/' + img_url
                categories_image.append(img_url)            

for data in categories_name:
    print(data)

for data in categories_image:
    print(data)