from django.conf.urls import url
import records.views as home_view


urlpatterns = [
    url(r'^$', home_view.home_view, name='home'),
    url(r'^document/(?P<shard>[0-9]{6})-(?P<docid>[\d]{14})',
        home_view.doc_view, name='document'),
]
