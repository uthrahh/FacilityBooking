from django.contrib.auth.hashers import make_password

from django.contrib import messages

from .forms import StartupSignupForm

from .models import Startup

def startup_signup(request):

    form = StartupSignupForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            startup = form.save(
                commit=False
            )

            startup.password_hash = (
                make_password(
                    form.cleaned_data[
                        "password"
                    ]
                )
            )

            startup.save()

            messages.success(
                request,
                "Account created successfully"
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