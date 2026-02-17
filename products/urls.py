from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('add_listing', views.add_listing, name="add_listing"),
]