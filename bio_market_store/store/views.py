from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse
from .models import UserProfile, Address, Product, MiniQuizBio, AddressOptional
from .forms import UserProfileForm, AddressForm, MiniQuizBioForm, UserPasswordChangeForm
from .utils.states import STATES
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.http import HttpResponse
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
            recipient_list=[settings.EMAIL_HOST_USER],
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
        description = request.POST.get("description")
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
                description,
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
            description=description,
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
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        try:
            validate_password(password)

            new_user = UserProfile.objects.create(
                username=username, email=email, role=role
            )
            new_user.set_password(password)
            new_user.save()

            messages.success(
                request,
                "You have been registered",
            )
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect("register")

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
    address_optional, created = AddressOptional.objects.get_or_create(user=request.user)
    address_form = AddressForm(instance=address)
    address_optional_form = AddressForm(instance=address_optional)
    password_form = PasswordChangeForm(request.user)

    return render(
        request,
        "user_profile.html",
        {
            "user_profile_form": user_profile_form,
            "address_form": address_form,
            "address_optional_form": address_optional_form,
            "password_form": password_form,
            "states": STATES,
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
                "state": address.state if address.state else "",
            }
            address_form = AddressForm(initial=address_data, instance=address)

    return render(
        request,
        "user_profile.html",
        {"address_form": address_form},
    )


@login_required
def user_profile_address_optional(request):
    address_optional, _ = AddressOptional.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address_optional)
        if form.is_valid():
            form.save()
            messages.success(request, "Alternative address updated successfully.")
            return redirect("user_profile")  # Przekierowanie z powrotem do profilu
    else:
        form = AddressForm(instance=address_optional)

    return render(request, "user_profile.html", {"address_optional_form": form})


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

def initialize_quiz_session(request):
    questions = MiniQuizBio.objects.order_by('?')[:5]
    request.session.update({
        "questions": [q.id for q in questions],
        "question_index": 0,
        "score": 0
    })

@login_required
def user_profile_delete_user(request):
    if "delete_attempts" not in request.session:
        request.session["delete_attempts"] = 0

    if request.method == "POST":
        input_password = request.POST.get("confirm-delete-password")
        user = request.user

        print("POST data:", request.POST)
        if check_password(input_password, user.password):
            user.delete()
            logout(request)
            messages.success(request, "Your account has been deleted successully!")
            request.session.pop("delete_attempts", None)
            return redirect("cover_page")
        else:
            request.session["delete_attempts"] += 1
            messages.error(
                request,
                f"Incorrect password. Attempt {request.session['delete_attempts']} of 3.",
            )

            if request.session["delete_attempts"] >= 3:
                logout(request)
                messages.error(
                    request, "Too many failed attempts. You have been logged out."
                )
                request.session.pop("delete_attempts", None)
                return redirect("cover_page")
    return redirect("user_profile")


def mini_quiz_bio_view(request):
    if "retry" in request.GET:
        for key in ["questions", "score", "question_index"]:
            request.session.pop(key, None)
        return redirect("mini_quiz_bio")

    if "questions" not in request.session:
        initialize_quiz_session(request)

    index = request.session["question_index"]
    total_questions = len(request.session["questions"])

    if index >= total_questions:
        return redirect("quiz_result")

    question = MiniQuizBio.objects.get(id=request.session["questions"][index])
    form = MiniQuizBioForm(request.POST or None, question=question)

    if request.method == "POST":
        if "submit" in request.POST and form.is_valid():
            selected = form.cleaned_data["answer"]
            correct = question.correct_answer
            request.session["score"] += 5 if selected == correct else 0

            messages.success(request, "✅ Correct!") if selected == correct else messages.error(
                request,
                f"❌ Incorrect! Correct answer: {correct.upper()} - {question.get_choices().get(correct, 'Unknown')}"
            )
            return redirect("mini_quiz_bio")

        if "next" in request.POST:
            request.session["question_index"] += 1
            return redirect("mini_quiz_bio")

        if "finish" in request.POST:
            return redirect("quiz_result")

    return render(request, "mini_quiz_bio.html", {
        "form": form,
        "question": question,
        "score": request.session["score"],
        "progress": (index / total_questions) * 100,
        "current_index": index + 1,
        "total_questions": total_questions,
    })


def quiz_result_view(request):
    score = request.session.get("score", 0)
    request.session.update({"score": 0, "question_index": 0})
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


@login_required
def payment(request):
    cart = request.session.get("cart", {})
    cart_items = []
    cart_total = 0
    total_items = 0
    user_profile = request.user
    address, created = Address.objects.get_or_create(user=request.user)
    address_optional, created = AddressOptional.objects.get_or_create(user=request.user)

    # Process cart items
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
        "user_profile": user_profile,
        "address": address,
        "address_optional": address_optional,
        "states": STATES,
    }

    if request.method == "POST":
        payment_method = request.POST.get("paymentMethod")
        address_type = request.POST.get("address_type", "billing")

        # Update user profile information
        user_profile.first_name = request.POST.get("firstName")
        user_profile.last_name = request.POST.get("lastName")
        user_profile.email = request.POST.get("email")
        user_profile.save()

        # Update the appropriate address based on selection
        if address_type == "billing":
            # Update billing address
            address.street = request.POST.get("address")
            address.postal_code = request.POST.get("zip")
            address.state = request.POST.get("state")
            address.city = request.POST.get("city")
            address.phone_number = request.POST.get("phoneNumber")
            address.save()

            # Use billing address for shipping
            selected_address = address
        else:
            # Update alternative address
            address_optional.street = request.POST.get("address_alt")
            address_optional.postal_code = request.POST.get("zip_alt")
            address_optional.state = request.POST.get("state_alt")
            address_optional.city = request.POST.get("city_alt")
            address_optional.phone_number = request.POST.get("phoneNumber_alt")
            address_optional.save()

            # Use alternative address for shipping
            selected_address = address_optional

        # Prepare email content
        products_info = "\n".join(
            [
                f"{idx + 1}. {item['name']} - {item['quantity']} szt. - {item['total']:.2f} PLN"
                for idx, item in enumerate(cart_items)
            ]
        )

        message_body = f"""
        New order from BioPotato Store:
        {"-" * 40}
        Customer: {user_profile.first_name} {user_profile.last_name}
        Contact: {selected_address.phone_number}

        Shipping Address:
        {selected_address.street}, {selected_address.city}, {selected_address.state}, {selected_address.postal_code}

        Payment Method: {payment_method}

        Order Details:
        {products_info}

        Total Order Value: {cart_total:.2f} PLN
        """

        # Send confirmation email
        try:
            send_mail(
                subject="New Order - BioPotato",
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            messages.warning(
                request, "Order processed, but confirmation email failed to send."
            )

        # Clear cart and redirect
        request.session["cart"] = {}
        messages.success(
            request, "Order completed successfully! Thank you for your purchase."
        )
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

def single_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return render(request, 'single_product.html', {'product': product})
    except Product.DoesNotExist:
        return HttpResponse(f"Product with id {product_id} does not exist.")

def about_project(request):
    return render(request, "about_project.html")