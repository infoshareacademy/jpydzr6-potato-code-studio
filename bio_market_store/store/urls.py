from django.urls import path
from .views import (
    cover_page,
    about_us,
    contact_us,
    home_page,
    register_view,
    login_view,
    logout_view,
    mini_quiz_bio_view,
    quiz_result_view,
    add_product,
    product_list,
)
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", home_page, name="home_page"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add/", add_product, name="add"),
    path("product_list/", product_list, name="product_list"),
    path("cover/", cover_page, name="cover-page"),
    path("cover/about/", about_us, name="about-page"),
    path("cover/contact", contact_us, name="contact-page"),
    path("quiz/", mini_quiz_bio_view, name="mini_quiz_bio"),
    path("quiz/result/", quiz_result_view, name="quiz_result"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
