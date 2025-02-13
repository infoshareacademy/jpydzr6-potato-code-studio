from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    re_path(r'^update_cart/(?P<product_id>\d+)/(?P<change>-?\d+)/$', views.update_cart, name='update_cart'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
]