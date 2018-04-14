from django.urls import path
from django.urls import re_path
from clients.views import index
from clients.views import ClientsList
from clients.views import ClientsDetail


urlpatterns = [
    path('', index, name='index'),
    re_path('api/?$', ClientsList.as_view(), name='list'),
    re_path('api/(?P<pk>[0-9]+)/?$', ClientsDetail.as_view(), name='detail'),
]