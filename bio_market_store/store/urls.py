from django.urls import path
from .views import home_page, register_view, login_view, logout_view, mini_quiz_bio_view, quiz_result_view

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("quiz/", mini_quiz_bio_view, name="mini_quiz_bio"),
    path("quiz/result/", quiz_result_view, name="quiz_result"),
]