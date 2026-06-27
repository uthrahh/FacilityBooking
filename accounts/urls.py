from django.urls import path

from .views import (
    startup_login,
    startup_signup,
    startup_dashboard,
    admin_login_view,
    logout_view,
)

urlpatterns = [

    # Startup Authentication

    path(
        "login/",
        startup_login,
        name="startup_login"
    ),

    path(
        "signup/",
        startup_signup,
        name="startup_signup"
    ),

    path(
        "dashboard/",
        startup_dashboard,
        name="startup_dashboard"
    ),

    # Admin Authentication

    path(
        "admin-login/",
        admin_login_view,
        name="admin_login"
    ),

    # Logout

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

]