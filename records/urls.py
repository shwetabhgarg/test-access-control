from django.conf.urls import url
import records.views as records_views


urlpatterns = [
    url(r'^$', records_views.home, name='home'),
]
