import django.conf.urls as urls

from scheduler.views.home_v import home
from scheduler.views.classroom_v import ClassroomListView
from scheduler.views.subject_v import SubjectListView

urlpatterns = [
    urls.url(r'^$', home, name='home'),
    urls.url(r'^classroom/$', ClassroomListView.as_view(), name='classroom_list'),
    urls.url(r'^subject/$', SubjectListView.as_view(), name='subject_list'),
]
