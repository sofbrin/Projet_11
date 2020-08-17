from django.contrib.auth.signals import user_logged_in

from .cart import FavoriteCart


def pending_favorites_handler(sender, request, user, *args, **kwargs):
    """Handles pending favorites saves after a successful connection."""
    request.user = user
    cart = FavoriteCart(request, user)
    cart.save_all()


# connection of the handler to signal
user_logged_in.connect(pending_favorites_handler)
