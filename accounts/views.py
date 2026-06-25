from django.shortcuts import render
from django.shortcuts import redirect

from startups.models import Startup
from django.contrib.auth.hashers import check_password
from .forms import StartupLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def startup_login(request):

    form = StartupLoginForm()

    error = None

    if request.method == "POST":

        form = StartupLoginForm(request.POST)

        if form.is_valid():

            startup_id = form.cleaned_data["startup_id"]
            password = form.cleaned_data["password"]

            try:

                startup = Startup.objects.get(
                    startup_id=startup_id,
                    is_active=True
                )

                if check_password(
                    password,
                    startup.password_hash
                ):
                    request.session["startup_id"] = startup.id

                    return redirect(
                        "/dashboard/"
                    )

                else:

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


def startup_dashboard(request):

    if not request.session.get("startup_id"):

        return redirect(
            "startup_login"
        )

    startup = Startup.objects.get(
        id=request.session["startup_id"]
    )

    return render(
        request,
        "accounts/dashboard.html",
        {
            "startup": startup
        }
    )

def admin_login_view(request):

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

        error = "Invalid Credentials"

    return render(
        request,
        "accounts/admin_login.html",
        {
            "error": error
        }
    )


def logout_view(request):

    logout(request)

    request.session.flush()

    return redirect(
        "startup_login"
    )

def logout_view(
    request
):

    request.session.flush()

    return redirect(
        "startup_login"
    )