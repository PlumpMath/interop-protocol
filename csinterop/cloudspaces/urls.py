from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers
from django.contrib import admin
from csinterop.views import SharingProposalViewSet

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'cloudspaces/share', SharingProposalViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cloudspaces.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^interop/', include('csinterop.urls')),
)
