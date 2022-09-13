from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from calorie.models import Category


class Command(BaseCommand):
    help = "collect categories"

    def handle(self, *args, **kwargs):
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

        count = 0
        length = len(categories_image)

        while count != length:
            try:
                Category.objects.create(
                    name = categories_name[count],
                    photo = categories_image[count]
                )
                print(categories_name[count])
                print(categories_image[count])
                count += 1
                print('added')
            except:
                print("don't added")
                count += 1
        self.stdout.write('complete')