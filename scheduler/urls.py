import django.conf.urls as urls

from scheduler.views import index


urlpatterns = [
    urls.url(r'^$', index, name='index'),
]
