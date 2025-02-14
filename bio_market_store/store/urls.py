
from django.urls import  path
from .views import cover_page, about_us, contact_us


from django.urls import path
from .views import home_page, register_view, login_view, logout_view
from .views import cover_page, about_us, contact_us, user_profile
from . import views

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', views.add_product, name="add"),
    path('profile/', views.user_profile, name="user_profile"),
    path('product_list/', views.product_list, name="product_list"),
    path("cover/", view=cover_page, name="cover-page"),
    path("cover/about/", view=about_us, name="about-page"),
    path("cover/contact", view=contact_us, name="contact-page"),
    ]

