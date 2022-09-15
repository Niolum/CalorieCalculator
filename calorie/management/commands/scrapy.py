from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from calorie.models import Category, Product
from django.core.files.base import ContentFile
import os


class Command(BaseCommand):
    help = "collect categories and products"

    def handle(self, *args, **kwargs):
        url = 'https://supercalorizator.ru/#'

        page = requests.get(url)

        categories_image = []
        categories_name = []

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')

            all_categories = soup.findAll('div', class_='main_block')
            for data in all_categories:
                if data.find('div', class_='menu_name'):
                    data = data.text.replace('\n', '')
                    categories_name.append(data)

            for data in all_categories:
                if data.find('div', class_='main_menu_image'):
                    img = data.find('img')
                    img_url = img.attrs.get('src')
                    img_url = 'https://supercalorizator.ru/' + img_url
                    categories_image.append(img_url)

            all_cat_divi = soup.findAll('divi', class_='main_block')
            for data in all_cat_divi:
                if data.find('div', class_='menu_name'):
                    data = data.text.replace('\n', '')
                    categories_name.append(data)

            for data in all_cat_divi:
                if data.find('div', class_='main_menu_image'):
                    img = data.find('img')
                    img_url = img.attrs.get('src')
                    img_url = 'https://supercalorizator.ru/' + img_url
                    categories_image.append(img_url)

            count_name = 0  
            div_img = len(categories_name) 
            while count_name != div_img:
                name_pict = categories_name[count_name]
                img_link = categories_image[count_name]
                with open(os.path.join('media/category', f'{name_pict}.png'), "wb") as f:
                    f.write(requests.get(img_link).content)
                    count_name += 1

            links = []

            all_categories = soup.findAll('div', class_='main_block')
            for data in all_categories:
                if data.find('a'):
                    link = url[:-1] + data.find('a').attrs.get('href')
                    links.append(link)

            all_cat_divi = soup.findAll('divi', class_='main_block')
            for data in all_cat_divi:
                if data.find('a'):
                    link = url[:-1] + data.find('a').attrs.get('href')
                    links.append(link)


        # Запись категорий в БД
        count = 0
        length = len(categories_image)

        while count != length:
            with open(os.path.join('media/category', f"{categories_name[count]}.png"), "rb") as f:
                data = f.read()
            try:
                Category.objects.get_or_create(
                    name = categories_name[count],
                    # photo = categories_image[count]
                    photo = Category.image.save(data)
                )
                print(categories_name[count])
                print(categories_image[count])
                count += 1
                print('added')
            except:
                print("don't added")
                count += 1
        self.stdout.write('complete')


        for link in links:
            cat_page = requests.get(link)

            soup = BeautifulSoup(cat_page.text, 'html.parser')

            category = soup.find('h1')
            category = category.text


            names = []
            images = []
            table = {'calorie': [], 'protein': [], 'fat': [], 'carbohydrate': []}
            descriptions = []
            product_urls = []

            all_name = soup.findAll('div', class_='product_name')
            for data in all_name:
                prod_name = data.text
                names.append(prod_name)

            all_image = soup.findAll('div', class_='product_image')
            for data in all_image:
                img = data.find('img')
                img_url = 'https://supercalorizator.ru/' + img.attrs.get('src')
                images.append(img_url)

            all_calorie = soup.findAll('span', class_='kkal_visible')
            for data in all_calorie:
                try:
                    data = float(data.text)
                except:
                    data = 0.0 
                table['calorie'].append(data)
                
            all_protein = soup.findAll('span', class_='bel_visible')
            for data in all_protein:
                try:
                    data = float(data.text)
                except:
                    data = 0.0 
                table['protein'].append(data)

            all_fat = soup.findAll('span', class_='fat_visible')
            for data in all_fat:
                try:
                    data = float(data.text)
                except:
                    data = 0.0 
                table['fat'].append(data)

            all_carbohydrate = soup.findAll('span', class_='ug_visible')
            for data in all_carbohydrate:
                try:
                    data = float(data.text)
                except:
                    data = 0.0 
                table['carbohydrate'].append(data)

            all_product = soup.findAll('a')
            for data in all_product:
                if data['href'].startswith('?product'):
                    product_urls.append(data['href'])

            for prod_url in product_urls:
                url_pr = 'https://supercalorizator.ru/' + prod_url
                descr_page = requests.get(url_pr)

                soup = BeautifulSoup(descr_page.text, 'html.parser')
                all_text = soup.find('div', id='prod_descr').text + soup.find('div', id='snoski').text + soup.find('div', id='for_diet').text
                descriptions.append(all_text)

            count_name = 0  
            count_img = len(images) 
            while count_name != count_img:
                name_pict = names[count_name]
                img_link = images[count_name]
                with open(os.path.join(f'media/product/{category}', f'{name_pict}.png'), "wb") as f:
                    f.write(requests.get(img_link).content)
                    count_name += 1


            # Запись продуктов в БД
            count = 0
            length = len(names)

            while count != length:
                with open(os.path.join(f"media/product/{category}", f"{names[count]}.png"), "rb") as f:
                    data = f.read()
                try:
                    Product.objects.get_or_create(
                        name = names[count],
                        # photo = images[count],
                        photo = Product.image.save(data),
                        calorie = table['calorie'][count],
                        fat = table['fat'][count],
                        protein = table['protein'][count],
                        carbohydrate = table['carbohydrate'][count],
                        category = Category.objects.get(name=category),
                        description = descriptions[count]
                    )
                    count += 1
                    print('added')
                except:
                    print("don't added")
                    count += 1
            self.stdout.write('complete')