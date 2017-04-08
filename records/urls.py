from django.conf.urls import url
import records.views as home_view


urlpatterns = [
    url(r'^$', home_view.HomeView.as_view(), name='home'),
    url(r'^document/(?P<shard>[0-9]{6})-(?P<docid>[\d]{14})/?$',
        home_view.DocumentView.as_view(), name='document'),
    url(r'^requests/?$', home_view.ApprovalRequestsView.as_view(), name='requests'),
]
