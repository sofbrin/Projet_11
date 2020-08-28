"""Helpers fonctions to make the use of the favoritecart app easier."""

from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import (
    redirect_to_login as auth_redirect_to_login,
)


# adapted from login_required decorator from django.contrib.auth.decorators
def redirect_to_login(
    request,
    favorite_url,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url=None,
):
    """Redirects the user to the login page."""
    resolved_favorite_url = resolve_url(favorite_url)
    resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)

    return auth_redirect_to_login(
        resolved_favorite_url, resolved_login_url, redirect_field_name
    )
