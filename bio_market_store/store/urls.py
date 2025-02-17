
from django.urls import  path
from .views import cover_page, about_us, contact_us


from django.urls import path
from .views import home_page, register_view, login_view, logout_view
from .views import cover_page, about_us, contact_us
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', views.add_product, name="add"),
    path('product_list/', views.product_list, name="product_list"),
    path("cover/", view=cover_page, name="cover-page"),
    path("cover/about/", view=about_us, name="about-page"),
    path("cover/contact", view=contact_us, name="contact-page"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('payment/', views.payment, name='payment'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

