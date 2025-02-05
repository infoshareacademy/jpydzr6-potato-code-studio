from django.urls import path
from . import views

urlpatterns = [










    path("products/", views.products, name="products"),
    path('add/', views.add_product, name="add"),
    path('product_list/', views.product_list, name="product_list"),
]
