from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('shop_logout',views.shop_logout),
    path('shop_home',views.shop_home),
    path('add_pet',views.add_pet),
    path('dog_list/<id>',views.dog_list),
]
