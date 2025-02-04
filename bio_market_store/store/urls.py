from django.urls import  path
from .views import cover_page, about_us, contact_us

urlpatterns = [
   path("cover/", view=cover_page, name="cover-page"),
   path("cover/about/", view=about_us, name="about-page"),
   path("cover/contact", view=contact_us, name="contact-page"),
]