from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    cover_page,
    about_us,
    contact_us,
    register_view,
    login_view,
    logout_view,
    user_profile,
    user_profile_personal_info,
    user_profile_address,
    user_profile_password,
    mini_quiz_bio_view,
    quiz_result_view,
    add_product,
    product_list,
    add_to_cart,
    empty_cart,
    payment,
    increment_quantity,
    decrement_quantity,
)

urlpatterns = [
    path("", cover_page, name="cover_page"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", user_profile, name="user_profile"),
    path(
        "profile/personal-info",
        user_profile_personal_info,
        name="user_profile_personal_info",
    ),
    path("profile/address", user_profile_address, name="user_profile_address"),
    path("profile/password", user_profile_password, name="user_profile_password"),
    path("add/", add_product, name="add"),
    path("product_list/", product_list, name="product_list"),
    path("about/", about_us, name="about-page"),
    path("contact", contact_us, name="contact-page"),
    path("quiz/", mini_quiz_bio_view, name="mini_quiz_bio"),
    path("quiz/result/", quiz_result_view, name="quiz_result"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('empty_cart/', empty_cart, name='empty_cart'),
    path('payment/', payment, name='payment'),
    path('increment_quantity/<int:product_id>/', increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:product_id>/', decrement_quantity, name='decrement_quantity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

