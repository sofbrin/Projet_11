"""Configuration module for the FavoriteCart app."""

from django.apps import AppConfig


class PendingFavoritesConfig(AppConfig):
    """Main config data structure for the pending_favorites app."""

    name = 'pending_favorites'

    def ready(self):
        """Initializations to be performed with the app is ready."""
        try:
            from . import signals
        except ImportError:
            pass
