from django.urls import path
from .views import home_page, register_view, login_view, logout_view, google_auth_receiver, google_sign_out

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('google-auth-receiver/', google_auth_receiver, name="google_auth_receiver"),
    path('google-logout/', google_sign_out, name="google_sign_out")
]