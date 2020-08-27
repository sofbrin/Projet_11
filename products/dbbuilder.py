import requests
from django.core.exceptions import ObjectDoesNotExist
from products.models import ProductDb, CategoryDb
from string import punctuation


def select_products():
    selected_products = []
    page = 1

    while len(selected_products) <= 5000:
        response = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params={
            'lang': 'fr',
            'nutriment_0': 'fat',
            'nutriment_compare_0': 'gte',
            'nutriment_value_O': 0,
            'nutriment_1': 'saturated-fat',
            'nutriment_compare_1': 'gte',
            'nutriment_value_0': 0,
            'nutriment_2': 'sugars',
            'nutriment_compare_2': 'gte',
            'nutriment_value_2': 0,
            'nutriment_3': 'salt',
            'nutriment_compare_3': 'gte',
            'nutriment_value_3': 0,
            'sort_b': 'unique_scans_n',
            'json': 1,
            'page_size': 1000,
            'action': 'process',
            'page': page,
            'fields': 'product_name,url,categories,image_front_url,nutrition_grades,code,nutriments'
        })
        data = response.json()
        products = data['products']

        for product in products:
            if 'product_name' not in product or product['product_name'] == '' \
                    or 'image_front_url' not in product or product['image_front_url'] == '' \
                    or 'nutrition_grades' not in product or product['nutrition_grades'] == '' \
                    or 'code' not in product or product['code'] == '' \
                    or len(product['categories']) < 3:
                continue
            else:
                selected_products.append(product)
                _save_in_db(product)

            if len(selected_products) == 5000:
                print(len(selected_products))
                break

        page += 1


def _save_in_db(product):
    product_name = clear_strings(product['product_name'])

    try:
        ProductDb.objects.get(name=product_name)
    except ObjectDoesNotExist:
        p = ProductDb.objects.create(name=product_name, url=product['url'],
                                     image=product['image_front_url'], nutriscore=product['nutrition_grades'],
                                     barcode=product['code'], fat=product['nutriments']['fat'],
                                     saturated_fat=product['nutriments']['saturated-fat'],
                                     sugar=product['nutriments']['sugars'], salt=product['nutriments']['salt'])

        prod_categories = product['categories'].split(',')
        for prod_category in prod_categories:
            prod_category = prod_category.strip()
            category = CategoryDb.objects.get_or_create(name=prod_category)[0]
            p.categories.add(category.id)


def clear_strings(name):
    product_name = name.lower()

    for character in punctuation:
        product_name = product_name.replace(character, " ")

    product_name = product_name.strip()

    return product_name




"""class ProductSelector:
    def __init__(self):
        self.url = 'https://fr.openfoodfacts.org/cgi/search.pl'
        self.params = {
            'lc': 'fr',
            'cc': 'fr',
            'nutriment_0': 'fat',
            'nutriment_compare_0': 'gte',
            'nutriment_value_O': 0,
            'nutriment_1': 'saturated-fat',
            'nutriment_compare_1': 'gte',
            'nutriment_value_0': 0,
            'nutriment_2': 'sugars',
            'nutriment_compare_2': 'gte',
            'nutriment_value_2': 0,
            'nutriment_3': 'salt',
            'nutriment_compare_3': 'gte',
            'nutriment_value_3': 0,
            'sort_b': 'unique_scans_n',
            'json': 1,
            'page_size': 1000,
            'action': 'process',
            'page': 1,
            'fields': 'product_name,url,categories,image_front_url,nutrition_grades,code,nutriments'
        }

    def select_products(self):
        response = requests.get(self.url, params=self.params)
        data = response.json()
        selected_products = data['products']

        for product in selected_products:
            if 'product_name' not in product or product['product_name'] == '' \
                    or 'image_front_url' not in product or product['image_front_url'] == ''\
                    or 'nutrition_grades' not in product or product['nutrition_grades'] == '' \
                    or 'code' not in product or product['code'] == '' \
                    or len(product['categories']) <= 3:
                continue
            else:
                self._save_in_db(product)

    def _save_in_db(self, product):
        product_name = product['product_name'].lower()

        try:
            ProductDb.objects.get(name=product_name)
        except ObjectDoesNotExist:
            try:
                p = ProductDb.objects.create(name=product_name, url=product['url'],
                                             image=product['image_front_url'], nutriscore=product['nutrition_grades'],
                                             barcode=product['code'], fat=product['nutriments']['fat'],
                                             saturated_fat=product['nutriments']['saturated-fat'],
                                             sugar=product['nutriments']['sugars'], salt=product['nutriments']['salt'])

                prod_categories = product['categories'].split(',')
                for prod_category in prod_categories:
                    category = CategoryDb.objects.get_or_create(name=prod_category)[0]
                    #print(category.id, category.name, category.url)
                    p.categories.add(category.id)

            except (ValidationError, AttributeError):
                pass"""



