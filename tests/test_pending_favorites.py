from django.test import TestCase
from django.urls import reverse

from pending_favorites.cart import FavoriteCart
from products.models import ProductDb, CategoryDb, UserPersonalDb
from users.models import User


class TestViewsPendingFavorites(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(first_name='Arthur', last_name='H',
                                             email='arthurH@gmail.com', password='1234')
        self.product = ProductDb.objects.create(id=49, name='nutella', url='', image='', nutriscore='d', barcode='',
                                                fat=0, saturated_fat=0, sugar=0, salt=0)
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='', product_count=0)
        self.product.categories.add(self.category)
        self.substitute = ProductDb.objects.create(id=50, name='noisette bio', url='', image='', barcode='',
                                                    nutriscore='b', fat=0, saturated_fat=0, sugar=0, salt=0)
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='', product_count=0)
        self.substitute.categories.add(self.category)

    def test_pending_fav(self):
        original_product = self.product.id
        replaced_product = self.substitute.id
        data = {'product_id': original_product, 'substitute_id': replaced_product}
        response = self.client.post(reverse('save_in_db'), data)
        # teste qu'il y a bien une redirection
        self.assertEqual(response.status_code, 302)
        # teste que la redirection renvoie sur l'url login
        self.assertIn(reverse('login'), response['Location'])
        # teste qu'il y a bien un nouvel élément dans la session enregistré sous la clé "fav cart"
        self.assertIn('__favorite_cart__', self.client.session)
        # teste que le dico contenu dans cet éément contient bien original product = product id
        self.assertEqual(data['product_id'], self.client.session['__favorite_cart__']['original_product'])
        # id pour substitute et replaced_ product
        self.assertEqual(data['substitute_id'], self.client.session['__favorite_cart__']['replaced_product'])




