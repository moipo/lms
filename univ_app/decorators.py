from django.http import HttpResponse


def allowed_users(allowed_groups: list = None):
    if allowed_groups is None:
        allowed_groups = []

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("У вас нет прав доступа к этой странице")

        return wrapper  #

    return decorator
