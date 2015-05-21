from django.conf.urls import patterns

urlpatterns = patterns('fatpages.views',
    (r'^(?P<url>.*)$', 'fatpage'),
)
