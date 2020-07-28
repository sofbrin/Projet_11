from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumlogin import force_login
from django.test import LiveServerTestCase
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from webdriver_manager.chrome import ChromeDriverManager

from products.models import ProductDb, CategoryDb, UserPersonalDb
from comments.models import CommentsDb
from users.models import User

#chrome_options = webdriver.ChromeOptions()
#chrome_options.headless = True


class SeleniumTests(LiveServerTestCase):
    """ Functional tests using the Chrome web browser in headless mode """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install())
        #cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        cls.selenium.implicitly_wait(10)
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='')
        self.product = ProductDb.objects.create(name='nutella', url='', image='', nutriscore='d', fat=0,
                                                saturated_fat=0, sugar=0, salt=0, category=self.category)
        self.comment_approved = CommentsDb.objects.create(text='je préfère le nutella bio', date='', author=self.user,
                                                          product=self.product, approved_comment=True)
        self.comment_not_approved = CommentsDb.objects.create(text='berkkkk', date='', author=self.user, product=self.product,
                                                              approved_comment=False)

    def test_link_product_redirects_OFF_detail_product(self):
        self.selenium.get('http://127.0.0.1:8000/products/product/352/')
        called_url = 'https://world.openfoodfacts.org/product/3272770003148/pure-goat-chavroux'
        self.selenium.find_element(By.LINK_TEXT, "Voir la fiche sur le site d'Open Food Facts").click()
        self.assertEqual(self.selenium.current_url, called_url)

        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('my_substitutes'))

    def test_use_django_selenium_login_to_force_login(self):
        #force_login(self.user, self.selenium, self.live_server_url)
        self.client.login(username='arthurH@gmail.com', password='1234')
        page_product = self.selenium.get(self.live_server_url + '/products/product/352')
        #page_product = self.selenium.get('{}/products/product/352'.format(live_server.url))
        text = self.selenium.find_element(By.NAME, 'text')
        text.send_keys("j'adore le fromage de chèvre")
        submit = self.selenium.find_element(By.ID, 'logforms')
        submit.click()
        self.assertEqual(self.selenium.current_url, page_product)

    """def test_comment_form_available_if_logged_in(self):
        user = User.objects.create_user(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        force_login(user, self.selenium, self.live_server.url)
        selenium.get()
        page_product = self.selenium.get('http://127.0.0.1:8000/products/product/352/')
        text = self.selenium.find_element(By.NAME, 'text')
        text.send_keys("j'adore le fromage de chèvre")
        submit = self.selenium.find_element(By.ID, 'logforms')
        submit.click()
        self.assertEqual(self.selenium.current_url, page_product)"""

    """def test_comment_form_not_available_if_not_logged_in(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        page_product = self.selenium.get('http://127.0.0.1:8000/products/product/352/')
        text = self.selenium.find_element(By.NAME, 'text')
        text.send_keys("j'adore le fromage de chèvre")
        submit = self.selenium.find_element(By.ID, 'logforms')
        submit.click()
        self.assertEqual(self.selenium.current_url, page_product)"""


class TestViewsProducts(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='')
        self.product = ProductDb.objects.create(name='nutella', url='', image='', nutriscore='d', fat=0,
                                                saturated_fat=0, sugar=0, salt=0, category=self.category)
        self.substitute1 = ProductDb.objects.create(name='nutella bio', url='', image='', nutriscore='a', fat=0,
                                                    saturated_fat=0, sugar=0, salt=0, category=self.category)
        ProductDb.objects.create(name='pâte noisette', url='', image='', nutriscore='b', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        ProductDb.objects.create(name='pâte choco', url='', image='', nutriscore='e', fat=0, saturated_fat=0,
                                 sugar=0, salt=0, category=self.category)
        self.comment = {'text': "j'aime pas le nutella", 'author': '', 'product': ''}
        self.comment_approved = CommentsDb.objects.create(text='je préfère le nutella bio', date='', author=self.user,
                                                          product=self.product, approved_comment=True)
        self.comment_not_approved = CommentsDb.objects.create(text='berkkkk', date='', author=self.user, product=self.product,
                                                              approved_comment=False)

    def test_product_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('product', args=(product_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product.html')

    def test_new_comment_is_saved_in_db(self):
        old_comments = CommentsDb.objects.count()
        product_id = self.product.id
        comment = self.comment
        user = self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.post(reverse('product', args=(product_id,)), {
            'text': comment,
            'author': user,
            'product': product_id
        })
        new_comments = CommentsDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_comments, old_comments + 1)

    """def test_approved_comment_is_displayed(self):
        product_id = self.product.id
        comment = self.comment_approved
        user = self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.post(reverse('product', args=(product_id,)), {
            'text': comment,
            'author': user,
            'product': product_id
        })

        self.assertEqual(response.status_code, 200)

    def test_new_comment_belongs_to_product(self):
        product_id = self.product.id
        user = self.client.login(username='arthurH@gmail.com', password='1234')
        comment = 'je préfère le nutella bio'
        response = self.client.post(reverse('product', args=(product_id,)), {
            'text': comment,
            'author': user,
            'product': product_id
        })
        item = CommentsDb.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comment, item.text)"""
        

    """def test_approved_comments_are_displayed(self):
        product_id = self.product.id
        self.comment_approved.product.id = product_id
        response = self.client.get(reverse('product', args=(product_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product.html')"""

    def test_my_substitutes_returns_200_user_logged_in(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/my_substitutes.html')

    def test_my_substitutes_returns_300_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('my_substitutes'))
        self.assertEqual(response.status_code, 302)

    def test_results_returns_better_nutriscore(self):
        product = self.product
        response = self.client.get(reverse('results'), {'query': product.name})
        context = response.context
        substitutes = context['substitutes']
        for substitute in substitutes:
            self.assertLess(substitute.nutriscore, product.nutriscore)

    def test_results_returns_200(self):
        product = self.product
        response = self.client.get(reverse('results'), {'query': product})
        self.assertEqual(response.status_code, 200)

    def test_search_returns_nothing(self):
        response = self.client.post(reverse('results'), {'query': ''})
        self.assertEqual(response.status_code, 302)

    def test_search_returns_unknown_product(self):
        product = 'unknown product'
        response = self.client.post(reverse('results'), {'query': product})
        self.assertEqual(response.status_code, 302)

    def test_save_in_db_returns_200(self):
        original_product = self.product.id
        replaced_product = self.substitute1.id
        self.client.login(username='arthurH@gmail.com', password='1234')
        previous_db_count = UserPersonalDb.objects.count()
        data = {'substitute_id': replaced_product, 'product_id': original_product}
        response = self.client.post(reverse('save_in_db'), data)
        new_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(previous_db_count + 1, new_db_count)

    def test_save_in_db_returns_prod_already_in_db(self):
        original_product = self.product.id
        replaced_product = self.substitute1.id
        self.client.login(username='arthurH@gmail.com', password='1234')
        previous_db_count = UserPersonalDb.objects.count()
        data = {'substitute_id': replaced_product, 'product_id': original_product}
        response = self.client.post(reverse('save_in_db'), data)
        response_json = response.json()
        new_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['is_created'])
        self.assertEqual(previous_db_count + 1, new_db_count)
        response2 = self.client.post(reverse('save_in_db'), data)
        response2_json = response2.json()
        last_db_count = UserPersonalDb.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response2_json['is_in_db'])
        self.assertEqual(new_db_count, last_db_count)


class IndexPageTest(SimpleTestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')


class LegalNoticeTest(SimpleTestCase):
    def test_legal_notice_returns_200(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/legal_notice.html')
