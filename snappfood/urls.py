from django.conf.urls import url
from django.urls import path
from snappfood.views import *

urlpatterns = [
   path('shop/list/', shop_list_view, name='shop-list'),
   path('register/', register_view, name='register'),
   path('login/', login_view, name='login'),
   path('profile/', profile_view, name='profile'),
   path('profile/edit/', edit_profile_view, name='edit-profile'),
   path('address/list/', address_list_view, name='address-list'),
   path('address/add/', address_add_view, name='address-add'),
   path('city/list/', city_list_view, name='city-list'),
   path('shop/list/', shop_list_view, name='shop-list'),
]
