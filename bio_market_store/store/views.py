from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import UserProfile, MiniQuizBio
from django.contrib.auth import authenticate, login, logout
import json
from store.forms import MiniQuizBioForm

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

def mini_quiz_bio_view(request):
    questions = list(MiniQuizBio.objects.all())
    index = request.session.get("question_index", 0)
    score = request.session.get("score", 0)
    message = request.session.pop("message", "")

    if index >= len(questions):
        return redirect("quiz_result")

    question = questions[index]
    try:
        choices = json.loads(question.answer_choices) if isinstance(question.answer_choices, str) else question.answer_choices
    except json.JSONDecodeError:
        choices = {}

    if request.method == "POST":
        form = MiniQuizBioForm(request.POST, question=question)

        if "submit" in request.POST and form.is_valid():
            selected = form.cleaned_data["answer"]
            correct = question.correct_answer

            if selected == correct:
                message = "✅ Correct!"
                score += 5
            else:
                message = f"❌ Incorrect! Correct answer: {correct.upper()}) {choices.get(correct, 'Unknown')}"

            request.session.update({"score": score, "message": message})

        elif "next" in request.POST:
            request.session["question_index"] = index + 1
            return redirect("mini_quiz_bio")

        elif "finish" in request.POST:
            return redirect("quiz_result")

    else:
        form = MiniQuizBioForm(question=question)

    return render(request, "mini_quiz_bio.html", {"form": form, "question": question, "message": message, "score": score})

def quiz_result_view(request):
    score = request.session.get("score", 0)

    request.session["score"] = 0
    request.session["question_index"] = 0

    return render(request, "quiz_result.html", {"score": score})
