from django.contrib.auth import login
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from users.tokens import account_activation_token

from users.forms import RegistrationForm, LoginForm
from users.models import User

from products.models import ProductDb, CategoryDb
from comments.models import CommentsDb

#chrome_options = webdriver.ChromeOptions()
#chrome_options.headless = True


"""class TestEmail(TestCase):
    def setUp(self):
        self.first_name = 'James'
        self.last_name = 'Bond'
        self.email = 'jbond@gmail.com'
        self.password = '1234'

        User.objects.create(first_name=self.first_name, last_name=self.last_name, email=self.email, password=self.password)

    def test_send_email(self):
        # send message
        mail.send_mail(
            'subject here', 'here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False
        )
        # test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        # verify that the subject of the message is correct
        self.assertEqual(mail.outbox[0].subject, 'subject here')
        # lien sur lequel l'utilisateur clique et que je peux récupérer dans test activate ?
        #self.assertEqual

    def test_activate_registration(self):
        user = User.objects.create_user(first_name='James', last_name='Bond', email='jbond@gmail.com', password='1234')
        user.is_active = False
        user.save()
        uid = force_text(urlsafe_base64_decode(self.uidb64))
        user = User.objects.get(pk=uid)
        account_activation_token.make_token(user)
        account_activation_token.check_token(user, self.token)
        #user.is_active = True
        #user.save()
        #contacter l'url avec self client .get

        self.assertTrue(user.is_active)


    def test_no_activation_without_link_confirmed(self):
        number_of_users = User.objects.count()
        user = User.objects.create_user(email='jbond@gmail.com', password='jbond1234')
        user.is_active = False
        new_number_of_users = User.objects.count()
        self.assertEqual(number_of_users, new_number_of_users)"""


"""class TestsSelenium(LiveServerTestCase):
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
        User.objects.create_user(email='jLennon@gmail.com', password='john1234')

    def test_signup_right_info(self):
        self.selenium.get(self.live_server_url + '/users/signup')
        first_name = self.selenium.find_element(By.NAME, 'first_name')
        last_name = self.selenium.find_element(By.NAME, 'last_name')
        email1 = self.selenium.find_element(By.NAME, 'email')
        password1 = self.selenium.find_element(By.NAME, 'password1')
        password2 = self.selenium.find_element(By.NAME, 'password2')
        submit = self.selenium.find_element(By.ID, 'logforms')
        first_name.send_keys('Robert')
        last_name.send_keys('Redford')
        email1.send_keys('rob@gmail.com')
        password1.send_keys('robert1234')
        password2.send_keys('robert1234')
        submit.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/users/signup')

    def test_signup_wrong_email(self):
        self.selenium.get(self.live_server_url + '/users/signup')
        first_name = self.selenium.find_element(By.NAME, 'first_name')
        last_name = self.selenium.find_element(By.NAME, 'last_name')
        email1 = self.selenium.find_element(By.NAME, 'email')
        password1 = self.selenium.find_element(By.NAME, 'password1')
        password2 = self.selenium.find_element(By.NAME, 'password2')
        submit = self.selenium.find_element(By.ID, 'logforms')
        first_name.send_keys('George')
        last_name.send_keys('Clooney')
        email1.send_keys('georgegmail.com')
        password1.send_keys('george1234')
        password2.send_keys('george1234')
        submit.click()
        try:
            error_email = self.selenium.find_element(By.XPATH, '//*[text()="Saisissez une adresse de courriel valide."]')
        except NoSuchElementException:
            self.fail('Impossible de trouver le message d\'erreur')
        self.assertTrue(error_email.is_displayed())

    def test_signup_wrong_password(self):
        self.selenium.get(self.live_server_url + '/users/signup')
        first_name = self.selenium.find_element(By.NAME, 'first_name')
        last_name = self.selenium.find_element(By.NAME, 'last_name')
        email1 = self.selenium.find_element(By.NAME, 'email')
        password1 = self.selenium.find_element(By.NAME, 'password1')
        password2 = self.selenium.find_element(By.NAME, 'password2')
        submit = self.selenium.find_element(By.ID, 'logforms')
        first_name.send_keys('Brad')
        last_name.send_keys('Pitt')
        email1.send_keys('brad@gmail.com')
        password1.send_keys('brad1234')
        password2.send_keys('brad123')
        submit.click()
        try:
            error_email = self.selenium.find_element(By.XPATH, '//*[text()="Les mots de passe ne correspondent pas. '
                                                              'Veuillez les saisir à nouveau."]')
        except NoSuchElementException:
            self.fail('Impossible de trouver le message d\'erreur')
        self.assertTrue(error_email.is_displayed())

    def test_login_right_info(self):
        self.selenium.get(self.live_server_url + '/users/login')
        email = self.selenium.find_element(By.NAME, 'email')
        password = self.selenium.find_element(By.NAME, 'password')
        submit = self.selenium.find_element(By.ID, 'logforms')
        email.send_keys('jLennon@gmail.com')
        password.send_keys('john1234')
        submit.click()
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/')

    def test_login_wrong_email_and_or_password(self):
        self.selenium.get(self.live_server_url + '/users/login')
        email = self.selenium.find_element(By.NAME, 'email')
        password = self.selenium.find_element(By.NAME, 'password')
        submit = self.selenium.find_element(By.ID, 'logforms')
        email.send_keys('johngmail.com')
        password.send_keys('john1234')
        submit.click()
        try:
            error_email = self.selenium.find_element(By.XPATH, '//*[text()="L\'email et/ou le mot de passe sont '
                                                              'invalides. Veuillez saisir à nouveau vos identifiants '
                                                              'ou créer un compte."]')
        except NoSuchElementException:
            self.fail('Impossible de trouver le message d\'erreur')
        self.assertTrue(error_email.is_displayed())


class TestModelsUserManager(TestCase):
    def test_username_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_create_manager(self):
        user = User.objects.create_user('arthurH@gmail.com', '1234', first_name='Arthur')
        self.assertEqual(user.email, 'arthurH@gmail.com')
        self.assertEqual(user.first_name, 'Arthur')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser('arthurH@gmail.com', '1234',  first_name='Arthur')
        self.assertEqual(superuser.email, 'arthurH@gmail.com')
        self.assertEqual(superuser.first_name, 'Arthur')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class TestFormsUsers(TestCase):

    def setUp(self):
        self.data1 = {
            'first_name': 'Arthur',
            'last_name': 'H',
            'email': 'arthurH@gmail.com',
            'password1': '1234',
            'password2': '1234'
        }
        self.data2 = {
            'email': 'arthurH@gmail.com',
            'password': '1234'
        }

    def test_regForm_is_valid(self):
        data = self.data1
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())

    def test_logForm_is_valid(self):
        data = self.data2
        form = LoginForm(data)
        self.assertTrue(form.is_valid())"""


class TestViewsUsers(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.token = account_activation_token.make_token(self.user)
        self.data1 = {'first_name': 'Thomas', 'last_name': 'Dutronc', 'email': 'thomasH@gmail.com',
                      'password1': '1234', 'password2': '1234'}
        self.data2 = {'email': 'arthurH@gmail.com', 'password': '1234'}
        self.data3 = {'uid': 'force_text(urlsafe_base64_encode(uidb64))'}

    def test_registration_returns_200(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_registration_post(self):
        data = self.data1
        response = self.client.post(reverse('signup'), data, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activez votre compte PurBeurre')
        self.assertEqual(response.status_code, 200)

    def test_activate(self):
        user = self.user
        user.is_active = False
        user.save()
        data = self.data3
        response = self.client.get('home', data)
        account_activation_token.check_token(self.user, self.token)
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, 302)

    """def test_login_ok(self):
        self.client.logout()
        data = self.data2
        response = self.client.post(reverse('login'), data, follow=True)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_logout_ok(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_account_returns_200(self):
        self.client.login(username='arthurH@gmail.com', password='1234')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_account_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)"""
