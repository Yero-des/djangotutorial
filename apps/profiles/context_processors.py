from django.contrib.auth import get_user_model

User = get_user_model()


def request_user(request):
    if not request.user.is_authenticated:
        return {}

    user = User.objects.select_related("config").get(pk=request.user.pk)

    return {
        "request_user": user,
    }
