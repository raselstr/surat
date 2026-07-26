from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from admin_berry.forms import LoginForm

from menus.forms import UserSelfProfileForm
from menus.models import UserProfile
from config.year_options import get_year_options, normalize_year


class ActiveYearLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_year = normalize_year(
            self.request.POST.get("active_year")
            or self.request.session.get("active_year")
        )
        context["year_options"] = get_year_options(extra_year=selected_year)
        context["selected_year"] = selected_year
        return context

    def form_valid(self, form):
        self.request.session["active_year"] = normalize_year(
            self.request.POST.get("active_year")
        )
        return super().form_valid(form)


@login_required
def set_active_year(request):
    if request.method == "POST":
        request.session["active_year"] = normalize_year(request.POST.get("active_year"))
        messages.success(request, "Tahun aktif berhasil diubah.")

    return redirect(request.POST.get("next") or request.META.get("HTTP_REFERER") or "/")


@login_required
def user_profile(request):
    UserProfile.objects.get_or_create(user=request.user)
    form = UserSelfProfileForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=request.user,
        request=request,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Profil berhasil diperbarui.")
        return redirect("user_profile")

    return render(request, "components/crud/form_page.html", {
        "form": form,
        "title": "Profil Saya",
        "permission": None,
        "url_list": "/",
        "form_action": request.path,
        "submit_label": "Simpan Profil",
        "is_multipart_form": form.is_multipart(),
        "use_modal": False,
        "template_form": "components/crud/form_general.html",
    })
