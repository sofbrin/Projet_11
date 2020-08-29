"""Helpers fonctions to make the use of the favoritecart app easier."""

from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import QueryDict, JsonResponse
from django.shortcuts import resolve_url


# adapted from login_required decorator from django.contrib.auth.decorators
def redirect_to_login(
    request,
    favorite_url,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url=None,
):
    """Build a JsonResponse indicating a redirection to login page.
    
    Prepare a json response indicating the js ajax response handler to 
    redirect to login with next target pointing to favorites.
    """
    resolved_favorite_url = resolve_url(favorite_url)
    resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
<<<<<<< HEAD
    login_url_parts = list(urlparse(resolved_login_url))

    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = resolved_favorite_url
        login_url_parts[4] = querystring.urlencode(safe='/')
=======
>>>>>>> 8dc53a3add633a3dcf391b215dfe301b9aba7c79

    return JsonResponse({
        "redirect": True,
        "follow": urlunparse(login_url_parts) 
    }, status=202)
