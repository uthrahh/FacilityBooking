from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.hashers import (
    check_password,
    make_password,
)

from django.contrib import messages

from startups.models import Startup

from .forms import (
    StartupLoginForm,
    StartupSignupForm,
)


def startup_login(request):

    if request.session.get("startup_id"):
        return redirect(
            "startup_dashboard"
        )

    form = StartupLoginForm()

    error = None

    if request.method == "POST":

        form = StartupLoginForm(
            request.POST
        )

        if form.is_valid():

            startup_id = form.cleaned_data[
                "startup_id"
            ]

            password = form.cleaned_data[
                "password"
            ]

            try:

                startup = Startup.objects.get(
                    startup_id=startup_id,
                    is_active=True
                )

                if check_password(
                    password,
                    startup.password_hash
                ):

                    request.session[
                        "startup_id"
                    ] = startup.id

                    request.session[
                        "startup_name"
                    ] = startup.name

                    messages.success(
                        request,
                        f"Welcome {startup.name}"
                    )

                    return redirect(
                        "startup_dashboard"
                    )

                error = "Invalid Password"

            except Startup.DoesNotExist:

                error = "Invalid Startup ID"

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "error": error
        }
    )


def startup_signup(request):

    form = StartupSignupForm()

    if request.method == "POST":

        form = StartupSignupForm(
            request.POST
        )

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        if form.is_valid():

            if password != confirm_password:

                messages.error(
                    request,
                    "Passwords do not match."
                )

            elif Startup.objects.filter(
                startup_id=form.cleaned_data[
                    "startup_id"
                ]
            ).exists():

                messages.error(
                    request,
                    "Startup ID already exists."
                )

            else:

                startup = form.save(
                    commit=False
                )

                startup.password_hash = (
                    make_password(
                        password
                    )
                )

                startup.is_active = True

                startup.save()

                messages.success(
                    request,
                    "Account created successfully."
                )

                return redirect(
                    "startup_login"
                )

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form
        }
    )


def admin_login_view(request):

    if request.user.is_authenticated:

        return redirect(
            "admin_dashboard"
        )

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_staff:

            login(
                request,
                user
            )

            return redirect(
                "admin_dashboard"
            )

        error = "Invalid Username or Password"

    return render(
        request,
        "accounts/admin_login.html",
        {
            "error": error
        }
    )


def startup_dashboard(request):

    if not request.session.get(
        "startup_id"
    ):

        return redirect(
            "startup_login"
        )

    startup = Startup.objects.get(
        id=request.session[
            "startup_id"
        ]
    )

    return render(
        request,
        "accounts/dashboard.html",
        {
            "startup": startup
        }
    )


def logout_view(request):

    logout(request)

    request.session.flush()

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect(
        "startup_login"
    )