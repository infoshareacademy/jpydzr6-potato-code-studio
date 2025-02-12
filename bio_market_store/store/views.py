import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from store.models import UserProfile

# Create your views here.
def home_page(request):
    return render(request, "index.html", {"google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID})

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        
        new_user = UserProfile.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        
        messages.success(request, "User created successfully")
        return redirect("home_page")

    return render(request, "register_page.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home_page")
        
        return render(request, "login_page.html", {"error": "Invalid username or password"})
            
    return render(request, "login_page.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful")
        return redirect("home_page")
    else:
        messages.error(request, "User is not authenticated")
        return redirect("home_page")
    
 
@csrf_exempt   
def google_auth_receiver(request):
    token = request.POST.get['credential']
    
    if not token:
        return HttpResponse("Missing token", status=400)
    
    try:
        user_data = id_token.verify_oauth2_token(token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID'])
    except ValueError:
        return HttpResponse(status=403)
    
    user, created = UserProfile.objects.get_or_create(email=user_data['email'])
    if created:
        user.username = user_data['name']
    
    login(request, user)
    return redirect('home_page')

def google_sign_out(request):
    request.session.flush()
    google_logout_url = "https://accounts.google.com/logout"
    return redirect(google_logout_url)