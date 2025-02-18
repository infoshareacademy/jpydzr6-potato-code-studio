from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import UserProfile, Address, Product
from .forms import UserProfileForm, AddressForm, MiniQuizBioForm
import json
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def home_page(request):
    return render(request, "index.html")


def cover_page(request):
    return render(request, "cover.html")


def about_us(request):
    return render(request, "about.html")


def contact_us(request):
    return render(request, "contact.html")


@login_required
def user_profile(request):
    user_profile = request.user
    address, created = Address.objects.get_or_create(user=user_profile)

    print(f"Current user: {request.user}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        address_form = AddressForm(request.POST, instance=address)
        if user_profile_form.is_valid() and address_form.is_valid():
            user_profile_form.save()
            address_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user_profile")
    else:
        user_profile_data = {
            "first_name": user_profile.first_name if user_profile.first_name else "",
            "last_name": user_profile.last_name if user_profile.last_name else "",
            "email": user_profile.email if user_profile.email else "",
        }
        address_data = {
            "street": address.street if address.street else "",
            "postal_code": address.postal_code if address.postal_code else "",
            "city": address.city if address.city else "",
            "phone_number": address.phone_number if address.phone_number else "",
        }
        user_profile_form = UserProfileForm(
            initial=user_profile_data, instance=user_profile
        )
        address_form = AddressForm(initial=address_data, instance=address)

    return render(
        request,
        "user_profile.html",
        {"user_profile_form": user_profile_form, "address_form": address_form},
    )


@login_required
def add_product(request):
    if request.method == "POST":
        name_tag = request.POST.get("name_tag")
        category = request.POST.get("category")
        price = request.POST.get("price")
        commission = request.POST.get("commission")
        weight = request.POST.get("weight")
        exp_date = request.POST.get("exp_date")
        amount = request.POST.get("amount")
        producer = request.POST.get("producer")
        image = request.FILES.get("image")

        if not all(
            [
                name_tag,
                category,
                price,
                commission,
                weight,
                exp_date,
                amount,
                producer,
                image,
            ]
        ):
            return render(request, "add_product.html")

        product = Product(
            user=request.user,
            name_tag=name_tag,
            category=category,
            price=price,
            commission=commission,
            weight=weight,
            exp_date=exp_date,
            amount=amount,
            producer=producer,
            image=image,
            created_at=now(),
        )

        product.save()

        return redirect("/product_list")

    return render(request, "add_product.html")


def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


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

        # new_user = UserProfile.objects.create_user(
        #     username=username, email=email, password=password
        # )
        new_user = UserProfile(username=username, email=email, is_active=False)
        new_user.set_password(password)
        new_user.save()

        logger.info(f"Username: {new_user}")
        print(f"Username: {new_user}")
        messages.success(
            request,
            "Zostałeś zarejestrowany, zaraz zostaniesz przeniesiony na Stronę Główną",
        )
        return redirect("home_page")

    return render(request, "register_page.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        logger.info(f"Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request,
                "Zostałeś zalogowany, zaraz zostaniesz przeniesiony na Stronę Główną",
            )
            return redirect("home_page")

        return render(
            request, "login_page.html", {"error": "Invalid username or password"}
        )

    return render(request, "login_page.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Zostałeś wylogowany")
        return redirect("home_page")
    else:
        messages.error(request, "User is not authenticated")
        return redirect("home_page")


def mini_quiz_bio_view(request):
    questions = list(MiniQuizBio.objects.all())
    question_index = request.session.get("question_index", 0)
    score = request.session.get("score", 0)
    message = request.session.pop("message", "")

    if question_index >= len(questions):
        return redirect("quiz_result")

    question = questions[question_index]
    correct_answer = question.correct_answer

    # Ensure answer choices are loaded properly
    answer_choices = (
        json.loads(question.answer_choices)
        if isinstance(question.answer_choices, str)
        else question.answer_choices
    )

    if request.method == "POST":
        form = MiniQuizBioForm(request.POST, question=question)

        if "submit" in request.POST:
            if form.is_valid():
                selected_answer = form.cleaned_data["answer"]

                if selected_answer == correct_answer:
                    message = "✅ Correct! Well done!"
                    score += 5
                else:
                    correct_answer_text = answer_choices.get(
                        correct_answer, "Unknown Answer"
                    )
                    message = f"❌ Incorrect! The correct answer is {correct_answer.upper()}) {correct_answer_text}"

                request.session["score"] = score
                request.session["message"] = message

        elif "next" in request.POST:
            request.session["question_index"] = question_index + 1
            return redirect("mini_quiz_bio")

        elif "finish" in request.POST:
            return redirect("quiz_result")

    else:
        form = MiniQuizBioForm(question=question)

    return render(
        request,
        "mini_quiz_bio.html",
        {"form": form, "question": question, "message": message, "score": score},
    )


def quiz_result_view(request):
    """Display the final quiz score and reset session."""
    score = request.session.get("score", 0)

    # Reset quiz progress
    request.session["score"] = 0
    request.session["question_index"] = 0

    return render(request, "quiz_result.html", {"score": score})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        new_user = UserProfile.objects.create_user(
            username=username, email=email, password=password
        )
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

        return render(
            request, "login_page.html", {"error": "Invalid username or password"}
        )

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

    if index >= len(questions):
        return redirect("quiz_result")

    question = questions[index]
    choices = question.get_choices()
    # try:
    #     choices = (
    #         json.loads(question.answer_choices)
    #         if isinstance(question.answer_choices, str)
    #         else question.answer_choices
    #     )
    # except json.JSONDecodeError:
    #     choices = {}

    if request.method == "POST":
        form = MiniQuizBioForm(request.POST, question=question)

        if "submit" in request.POST and form.is_valid():
            selected = form.cleaned_data["answer"]
            correct = question.correct_answer

            if selected == correct:
                score += 5
                request.session["score"] = score
                messages.success(request, "✅ Correct!")
            else:
                correct_answer_text = correct if correct in choices else "Unknown"
                messages.warning(
                    request,
                    f"❌ Incorrect! Correct answer: {correct.upper()} {correct_answer_text}",
                )

        elif "next" in request.POST:
            request.session["question_index"] = index + 1
            return redirect("mini_quiz_bio")

        elif "finish" in request.POST:
            return redirect("quiz_result")

    else:
        form = MiniQuizBioForm(question=question)

    return render(
        request,
        "mini_quiz_bio.html",
        {"form": form, "question": question, "score": score},
    )


def quiz_result_view(request):
    score = request.session.get("score", 0)

    request.session["score"] = 0
    request.session["question_index"] = 0

    return render(request, "quiz_result.html", {"score": score})
