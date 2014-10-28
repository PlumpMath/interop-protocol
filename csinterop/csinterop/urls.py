from django.conf.urls import patterns, url

urlpatterns = patterns(
    'csinterop.views',
    url(r'^proposal/(?P<key>[\w-]+)/$', 'proposal_view', name='proposal_view'),
    url(r'^result/$', 'proposal_result', name='proposal_result'),
    url(r'^select/(?P<key>[\w-]+)/$', 'proposal_select', name='proposal_select'),
    url(r'^share/$', 'proposal_share', name='proposal_share'),
    url(r'^credentials/$', 'proposal_credentials', name='proposal_credentials'),
)