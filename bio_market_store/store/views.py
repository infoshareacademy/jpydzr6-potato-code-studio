from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import UserProfile
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home_page(request):
    return render(request, "index.html")

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