from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse
from .models import UserProfile, Address, Product, MiniQuizBio
from .forms import UserProfileForm, AddressForm, MiniQuizBioForm, UserPasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings

# import json
import logging

logger = logging.getLogger(__name__)


def cover_page(request):
    return render(request, "cover.html")


def about_us(request):
    return render(request, "about.html")


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"Od: {name} <{email}>\n Temat: {subject}\n\n{message}"

        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            ["biopotato@wp.pl"],
        )

        return render(request, "contact.html", {"success": True})

    return render(request, "contact.html")


@login_required
def add_product(request):
    if request.method == "POST":
        name_tag = request.POST.get("name_tag")
        category = request.POST.get("category")
        price = request.POST.get("price")
        commission = 10
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
    cart = request.session.get("cart", {})

    total_items = 0
    cart_total = 0.0

    # Calculate total items and cart total
    for item in cart.values():
        total_items += item["quantity"]
        cart_total += float(item["price"]) * item["quantity"]

    return render(
        request,
        "product_list.html",
        {"products": products, "cart_total": cart_total, "total_items": total_items},
    )


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

        messages.success(
            request,
            "You have been registered",
        )
    return render(request, "register_page.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "login_page.html")

        login(request, user)
        messages.success(
            request,
            "You have been logged in",
        )

    return render(request, "login_page.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out")
        return redirect("cover_page")


@login_required
def user_profile(request):
    user_profile_form = UserProfileForm(instance=request.user)
    address, created = Address.objects.get_or_create(user=request.user)
    address_form = AddressForm(instance=address)
    password_form = PasswordChangeForm(request.user)

    return render(
        request,
        "user_profile.html",
        {
            "user_profile_form": user_profile_form,
            "address_form": address_form,
            "password_form": password_form,
        },
    )


@login_required
def user_profile_personal_info(request):
    user_profile = request.user
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user_profile")
    else:
        user_profile_data = {
            "first_name": user_profile.first_name if user_profile.first_name else "",
            "last_name": user_profile.last_name if user_profile.last_name else "",
            "email": user_profile.email if user_profile.email else "",
        }
        user_profile_form = UserProfileForm(
            initial=user_profile_data, instance=user_profile
        )

    return render(
        request,
        "user_profile.html",
        {"user_profile_form": user_profile_form},
    )


@login_required
def user_profile_address(request):
    user_profile = request.user
    address, created = Address.objects.get_or_create(user=user_profile)
    if request.method == "POST":
        address_form = AddressForm(request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user_profile")
        else:
            address_data = {
                "street": address.street if address.street else "",
                "postal_code": address.postal_code if address.postal_code else "",
                "city": address.city if address.city else "",
                "phone_number": address.phone_number if address.phone_number else "",
            }
            address_form = AddressForm(initial=address_data, instance=address)

    return render(
        request,
        "user_profile.html",
        {"address_form": address_form},
    )


@login_required
def user_profile_password(request):
    if request.method == "POST":
        password_form = UserPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "The password was changed successfully!")
            return redirect("user_profile")
        else:
            if "old_password" in password_form.errors:
                messages.error(request, "The old password is incorrect.")
            if "new_password2" in password_form.errors:
                messages.error(request, "New password and confirmation do not match.")

            return redirect("user_profile")

    password_form = UserPasswordChangeForm(request.user)
    return render(request, "user_profile.html", {"password_form": password_form})


def mini_quiz_bio_view(request):
    questions = list(MiniQuizBio.objects.all().order_by('?')[:5])
    index = request.session.get("question_index", 0)
    score = request.session.get("score", 0)

    if index >= len(questions):
        return redirect("quiz_result")

    question = questions[index]
    choices = question.get_choices()

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
                correct_answer_text = choices.get(correct, "Unknown")
                messages.error(
                    request,
                    f"❌ Incorrect! Correct answer: {correct.upper()} - {correct_answer_text}",
                )

            # ✅ Stay on the same question (don't increment index)
            return render(
                request,
                "mini_quiz_bio.html",
                {"form": form, "question": question, "score": score},
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


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})

    product_key = str(product_id)

    if product_key in cart:
        cart[product_key]["quantity"] += 1
    else:
        cart[product_key] = {
            "quantity": 1,
            "price": str(product.price),
            "name": product.name_tag,
            "image": product.image.url,
        }

    request.session["cart"] = cart
    request.session.modified = True  # Critical fix
    return redirect("product_list")


def empty_cart(request):
    if "cart" in request.session:
        del request.session["cart"]
    return redirect("product_list")


def payment(request):
    cart = request.session.get("cart", {})

    cart_items = []
    cart_total = 0
    total_items = 0

    for product_id, item in cart.items():
        total = float(item["price"]) * item["quantity"]
        cart_total += total
        total_items += item["quantity"]

        cart_items.append(
            {
                "id": product_id,
                "name": item["name"],
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "total": total,
            }
        )

    context = {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "total_items": total_items,
    }

    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        phone = request.POST.get("phoneNumber")
        email = request.POST.get("email")
        address = request.POST.get("address")
        address2 = request.POST.get("address2", "")
        country = request.POST.get("country")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip")
        payment_method = request.POST.get("paymentMethod")
        products_info = "\n".join(
            [
                f"{idx + 1}. {item['name']} - {item['quantity']} szt. - {item['total']} PLN"
                for idx, item in enumerate(cart_items)
            ]
        )

        message_body = f"""
        New order from BioMarket Store:

        First Name: {first_name}
        Last Name: {last_name}
        Contact Number: {phone}
        Email: {email}
        Address: {address}
        Address 2: {address2}
        Country: {country}
        State: {state}
        Zip: {zip_code}
        Payment method: {payment_method}

        Oreder details:
        \n{products_info}

        Oder value: {sum(item["total"] for item in cart_items):.2f} PLN
        """

        send_mail(
            subject="Nowe zamówienie",
            message=message_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["biopotato@wp.pl"],
            fail_silently=False,
        )

        request.session["cart"] = {}

        return redirect("product_list")

    return render(request, "payment.html", context=context)


def increment_quantity(request, product_id):
    product_key = str(product_id)
    cart = request.session.get("cart", {})
    if product_key in cart:
        cart[product_key]["quantity"] += 1
        request.session["cart"] = cart
        request.session.modified = True

        # Calculate total items and cart total
        total_items = sum(item["quantity"] for item in cart.values())
        cart_total = sum(
            float(item["price"]) * item["quantity"] for item in cart.values()
        )

        return JsonResponse(
            {
                "quantity": cart[product_key]["quantity"],
                "total": float(cart[product_key]["price"])
                * cart[product_key]["quantity"],
                "cart_total": cart_total,
                "total_items": total_items,
            }
        )
    return JsonResponse({"error": "Product not found in cart"}, status=404)


def decrement_quantity(request, product_id):
    product_key = str(product_id)
    cart = request.session.get("cart", {})
    if product_key in cart:
        if cart[product_key]["quantity"] > 1:
            cart[product_key]["quantity"] -= 1
        else:
            # Instead of deleting the item, set its quantity to 0
            cart[product_key]["quantity"] = 0
        request.session["cart"] = cart
        request.session.modified = True

        # Calculate total items and cart total
        total_items = sum(item["quantity"] for item in cart.values())
        cart_total = sum(
            float(item["price"]) * item["quantity"] for item in cart.values()
        )

        return JsonResponse(
            {
                "quantity": cart.get(product_key, {}).get("quantity", 0),
                "total": float(cart.get(product_key, {}).get("price", 0))
                * cart.get(product_key, {}).get("quantity", 0),
                "cart_total": cart_total,
                "total_items": total_items,
            }
        )
    return JsonResponse({"error": "Product not found in cart"}, status=404)
