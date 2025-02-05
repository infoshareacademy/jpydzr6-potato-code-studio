from django.urls import path
from .views import home_page, register_view, login_view, logout_view
from . import views

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', views.add_product, name="add"),
    path('product_list/', views.product_list, name="product_list"),
