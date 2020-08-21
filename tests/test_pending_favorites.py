from django.test import TestCase
from django.urls import reverse

from pending_favorites.cart import FavoriteCart
from products.models import ProductDb, CategoryDb, UserPersonalDb
from users.models import User


class TestViewsPendingFavorites(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='Arthur', last_name='H', email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.product = ProductDb.objects.create(id=49, name='nutella', url='', image='', nutriscore='d', barcode='',
                                                fat=0, saturated_fat=0, sugar=0, salt=0)
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='', product_count=0)
        self.product.categories.add(self.category)
        self.substitute = ProductDb.objects.create(id=50, name='noisette bio', url='', image='', barcode='',
                                                    nutriscore='b', fat=0, saturated_fat=0, sugar=0, salt=0)
        self.category = CategoryDb.objects.create(name='pâte à tartiner', url='', product_count=0)
        self.substitute.categories.add(self.category)

    def test_pending_fav_returns_302(self):
        request = self.product
        cart = FavoriteCart(request)
        cart.add(
            {
                "original_product": self.product.id,
                "replaced_product": self.substitute.id,
                "user": "user",
            }
        )
        response = self.client.post('save_in_db', cart)
        self.assertIn(response, self.client.session)
        self.assertEqual(response.status_code, 302)