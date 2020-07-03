from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.register_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('account', views.account_view, name='account'),
    path('email_activation/<uid64>/<token>/', views.activate, name='activate'),
    #url(r'^email_activation/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate')
]
