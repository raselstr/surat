from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin:index")

    return render(request, "pages/index.html")
