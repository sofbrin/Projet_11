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
    # If the login url is the same scheme and net location then just
    # use the path as the "next" url.
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    favorite_scheme, favorite_netloc = urlparse(resolved_favorite_url)[:2]
    if (not login_scheme or login_scheme == favorite_scheme) and (
        not login_netloc or login_netloc == favorite_netloc
    ):
        resolved_favorite_url = request.get_full_path()

    return auth_redirect_to_login(
        resolved_favorite_url, resolved_login_url, redirect_field_name
    )
