from django.urls import path
from . import views

urlpatterns=[
    path('shop_login',views.shop_login),
    path('shop_logout',views.shop_logout),
    path('shop_home',views.shop_home),
    path('dog_list/<id>',views.dog_list),
    path('add_pet',views.add_pet),
    path('edit_pet/<id>/', views.edit_pet),
    # path('delete',views.delete),
    path('register',views.register),
    path('',views.user_home),
]
