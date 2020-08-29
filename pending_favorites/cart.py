from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class FavoriteCart:
    """Implements a cart storing pending favorites into session."""

    CART_SESSION_ID = '__favorite_cart__'

    def __init__(self, request, user=None):
        """Initializes the cart to store favorites."""
        self.user = user or request.user
        self.request = request
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[self.CART_SESSION_ID] = []
        self.cart = cart

    def add(self, favorite):
        """Adds a favorite."""
        self.cart.append(favorite)
        self.session.modified = True
        """messages.success(
            self.request, 'Le produit a été placé dans votre panier, '
                     'il sera entregistré dans votre espace '
                     'quand vous vous connecterez.',
            extra_tags='toaster')"""

    def clear(self):
        """Removes the cart from the session."""
        self.cart.clear()
        self.session.modified = True

    def save_all(self):
        """save all pending favorites into database."""
        if not self.user.is_authenticated:
            return

        # fetch the favorite and favorited models from the specs in settings
        favorite_model = self._get_model('favorite')
        favorited_model = self._get_model('favorited')

        # Save all pending favorites in database
        for favorite in self.cart:
            for key in favorite:
                if favorite[key] == "user":
                    favorite[key] = self.request.user
                else:
                    favorite[key] = favorited_model.objects.get(
                        pk=favorite[key]
                    )
            favorite_model.objects.get_or_create(**favorite)
        # Empty the cart
        self.clear()

    def __iter__(self):
        """Iterates over the favorite items in the cart."""
        return iter(self.cart)

    def __len__(self):
        return len(self.cart)

    def _get_model(self, constant_name):
        """Returns the model specified with constant_name in the settings."""
        constant_name = f"{constant_name}_MODEL".upper()
        model_name = getattr(settings, constant_name)
        try:
            return django_apps.get_model(model_name, require_ready=False)
        except ValueError:
            raise ImproperlyConfigured(
                f"{constant_name} must be of the form 'app_label.model_name'"
            )
        except LookupError:
            raise ImproperlyConfigured(
                f"{constant_name} refers to model '{model_name}' "
                "that has not been installed"
            )
