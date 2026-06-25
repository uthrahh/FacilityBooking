from django.urls import path

from .views import (
    startup_login,
    startup_dashboard
)
from .views import (
    admin_login_view,
    logout_view
)
from .views import (
    startup_login,
    startup_dashboard,
    logout_view
)
urlpatterns = [
    path(
        "login/",
        startup_login,
        name="startup_login"
    ),
    path(
        "dashboard/",
        startup_dashboard,
        name="startup_dashboard"
    ),
    path(
        "admin-login/",
        admin_login_view,
        name="admin_login"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),
    path(
        "logout/",
        logout_view,
        name="logout"
    ),
]