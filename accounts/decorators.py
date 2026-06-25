from django.shortcuts import redirect

from django.shortcuts import redirect


def admin_login_required(view_func):

    def wrapper(
        request,
        *args,
        **kwargs
    ):

        if not request.user.is_authenticated:

            return redirect(
                "admin_login"
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper

def startup_login_required(
    view_func
):

    def wrapper(
        request,
        *args,
        **kwargs
    ):

        if not request.session.get(
            "startup_id"
        ):
            return redirect(
                "startup_login"
            )

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper