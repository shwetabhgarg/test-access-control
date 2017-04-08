from re import compile as re_compile
from django.conf import settings
from django.shortcuts import redirect


EXEMPT_URLS = [settings.LOGIN_URL.strip('/'), 'admin/*']
EXEMPT_URLS = [re_compile(e) for e in EXEMPT_URLS]

def auth_required_middleware(get_response):

    def ensure_request(request):
        if not request.user.is_authenticated():
            path = request.path_info.strip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        return get_response(request)

    return ensure_request
