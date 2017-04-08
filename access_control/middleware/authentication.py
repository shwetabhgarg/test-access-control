from django.http import HttpResponseRedirect
from django.conf import settings


EXEMPT_URLS = [settings.LOGIN_URL.lstrip('/')]

def auth_required_middleware(get_response):

    def ensure_request(request):
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if path not in EXEMPT_URLS:
                return HttpResponseRedirect(settings.LOGIN_URL)
        return get_response(request)

    return ensure_request
