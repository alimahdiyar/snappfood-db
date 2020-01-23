from django.conf.urls import url
from django.urls import path
from snappfood.views import *

urlpatterns = [
   path('shop/list/', shop_list_view, name='shop-list'),
   path('register/', register_view, name='sregister'),
   path('address/list/', address_list_view, name='address-list'),
   path('address/add/', address_add_view, name='address-add'),
   path('shop/list/', shop_list_view, name='shop-list'),
]
