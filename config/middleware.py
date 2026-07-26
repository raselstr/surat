from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


class SessionSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout_seconds = getattr(settings, "IDLE_TIMEOUT_SECONDS", 1800)

    def __call__(self, request):
        if self._is_asset_path(request.path):
            return self.get_response(request)

        if self._is_public_path(request.path):
            response = self.get_response(request)
            return self._set_no_cache_headers(response)

        if not request.user.is_authenticated:
            return self._build_login_redirect(request)

        if self._is_session_expired(request):
            logout(request)
            return self._build_login_redirect(request, expired=True)

        request.session["last_activity"] = int(timezone.now().timestamp())

        response = self.get_response(request)
        return self._set_no_cache_headers(response)

    def _is_public_path(self, path):
        public_paths = {
            reverse("masuk"),
            reverse("logout"),
            reverse("timeout_logout"),
        }
        
        if path.startswith("/api/"):
            return True

        if path in public_paths or path == "/favicon.ico":
            return True

        return False

    def _is_asset_path(self, path):
        asset_prefixes = [
            settings.STATIC_URL,
            settings.MEDIA_URL,
        ]
        return any(path.startswith(prefix) for prefix in asset_prefixes if prefix)

    def _is_session_expired(self, request):
        last_activity = request.session.get("last_activity")
        if not last_activity:
            return False

        now_timestamp = int(timezone.now().timestamp())
        return now_timestamp - int(last_activity) > self.timeout_seconds

    def _build_login_redirect(self, request, expired=False):
        login_url = reverse("masuk")
        query_params = {}

        if expired:
            query_params["expired"] = "1"
        elif request.path not in {"/", login_url}:
            query_params["next"] = request.get_full_path()

        target_url = login_url
        if query_params:
            target_url = f"{login_url}?{urlencode(query_params)}"

        if getattr(request, "htmx", False):
            response = HttpResponse(status=204)
            response["HX-Redirect"] = target_url
            return self._set_no_cache_headers(response)

        response = redirect(target_url)
        return self._set_no_cache_headers(response)

    def _set_no_cache_headers(self, response):
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response


class SecurityHeadersMiddleware:
    """
    Menambahkan header keamanan dasar untuk mengurangi risiko
    XSS, clickjacking, MIME sniffing, dan penyalahgunaan fitur browser.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp_directives = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
            "img-src 'self' data: blob:; "
            "font-src 'self' data: https://cdn.jsdelivr.net; "
            "connect-src 'self' https://nominatim.openstreetmap.org; "
            "frame-src 'self' https://www.openstreetmap.org; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "object-src 'none'"
        )

        if getattr(settings, "USE_HTTPS", False):
            csp_directives = f"{csp_directives}; upgrade-insecure-requests"

        response.setdefault(
            "Content-Security-Policy",
            csp_directives,
        )
        response.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(self), payment=(), usb=()",
        )
        response.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        response.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        response.setdefault("Referrer-Policy", "same-origin")
        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("X-Permitted-Cross-Domain-Policies", "none")
        return response
