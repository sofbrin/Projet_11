from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.test import LiveServerTestCase
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from webdriver_manager.chrome import ChromeDriverManager

from products.models import ProductDb, CategoryDb, UserPersonalDb
from comments.models import CommentsDb
from users.models import User


class SeleniumTests(LiveServerTestCase):
    """ Functional tests using the Chrome web browser in headless mode """
    """@classmethod
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
        self.product = ProductDb.objects.create(id=49, name='nutella', url='', image='', nutriscore='d', fat=0,
                                                saturated_fat=0, sugar=0, salt=0, category=self.category)
        self.substitut = ProductDb.objects.create(id=50, name='noisette bio', url='', image='', nutriscore='b', fat=0,
                                                  saturated_fat=0, sugar=0, salt=0, category=self.category)

    def test_form_comment_available_if_logged_in(self):
        self.selenium.get(self.live_server_url + '/users/login')
        email = self.selenium.find_element(By.NAME, 'email')
        password = self.selenium.find_element(By.NAME, 'password')
        submit = self.selenium.find_element(By.ID, 'logforms')
        email.send_keys('arthurH@gmail.com')
        password.send_keys('1234')
        submit.click()
        page_product = self.live_server_url + '/products/product/50/'
        self.selenium.get(page_product)
        text = self.selenium.find_element(By.NAME, 'text')
        text.send_keys("je préfère le nutella")
        submit = self.selenium.find_element(By.ID, 'logforms')
        submit.click()
        text_mod = 'Votre commentaire est en attente de modération'
        page_text_mod = self.selenium.find_element(By.ID, 'moderation')
        self.assertEqual(text_mod, page_text_mod.text)

    def test_form_comment_not_available_if_not_logged_in(self):
        page_product = self.live_server_url + '/products/product/49/'
        self.selenium.get(page_product)
        text_mod = 'Vous devez être connecté pour laisser un commentaire.'
        page_text_mod = self.selenium.find_element(By.ID, 'noform')
        self.assertEqual(text_mod, page_text_mod.text)


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

    def test_approved_comment_is_displayed(self):
        product_id = self.product.id
        comment = self.comment_approved
        user = self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.post(reverse('product', args=(product_id,)), {
            'text': comment,
            'author': user,
            'product': product_id
        })
        self.assertEqual(response.status_code, 200)

    def test_not_approved_comment_not_displayed(self):
        product_id = self.product.id
        comment = self.comment_not_approved
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
