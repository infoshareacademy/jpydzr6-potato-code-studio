from django.urls import path
from .views import (
    # home_page,
    register_view,
    login_view,
    logout_view,
    cover_page,
    about_us,
    contact_us,
    add_product,
    product_list,
)

urlpatterns = [
    # path("", home_page, name="home_page"),
    path("", cover_page, name="cover-page"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add/", add_product, name="add"),
    path("product_list/", product_list, name="product_list"),
    path("about/", about_us, name="about-page"),
    path("contact", contact_us, name="contact-page"),
]
