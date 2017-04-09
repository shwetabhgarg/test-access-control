from django.conf.urls import url
import records.views.access as access_view
import records.views.home as home_view
import records.views.documents as doc_view


urlpatterns = [
    url(r'^$', home_view.HomeView.as_view(), name='home'),
    url(r'^document/(?P<shard>[0-9]{6})-(?P<docid>[\d]{14})/?$',
        doc_view.DocumentView.as_view(), name='document'),
    url(r'^document/(?P<shard>[0-9]{6})-(?P<docid>[\d]{14})/share/?$',
        access_view.ShareView.as_view(), name='share'),
    url(r'^requests/?$', access_view.ApprovalRequestsView.as_view(), name='requests'),
]
