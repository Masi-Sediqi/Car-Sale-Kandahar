from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('add_listing', views.add_listing, name="add_listing"),
    path('shop', views.shop, name="shop"),
    path('delete_car/<int:id>/', views.delete_car, name="delete_car"),
    path('edit_car/<int:id>/', views.edit_car, name="edit_car"),
    path('car_detail/<int:id>/', views.car_detail, name="car_detail"),
    path('toggle_wishlist/<int:car_id>/', views.toggle_wishlist, name="toggle_wishlist"),
    path('my_wishlist/', views.my_wishlist, name="my_wishlist"),
]