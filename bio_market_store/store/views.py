from django.shortcuts import render

# Create your views here.


def cover_page(request):
    return render(request, 'store/cover.html')

def about_us(request):
    return render(request, 'store/about.html')

def contact_us(request):
    return render(request, 'store/contact.html')