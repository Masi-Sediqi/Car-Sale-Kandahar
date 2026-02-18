from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('add_listing', views.add_listing, name="add_listing"),
    path('shop', views.shop, name="shop"),
    path('delete_car/<int:id>/', views.delete_car, name="delete_car"),
    path('car_detail/<int:id>/', views.car_detail, name="car_detail"),
]