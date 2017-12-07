import django.conf.urls as urls

from scheduler.views.home_v import home
from scheduler.views.classroom_v import ClassroomListView, update_classroom
from scheduler.views.subject_v import SubjectListView, update_subject

urlpatterns = [
    urls.url(r'^$', home, name='home'),
    urls.url(r'^classroom/$', ClassroomListView.as_view(), name='classroom_list'),
    urls.url(r'^classroom/update$', update_classroom, name='update_classroom'),
    urls.url(r'^subject/$', SubjectListView.as_view(), name='subject_list'),
    urls.url(r'^subject/update$', update_subject, name='update_subject'),
]
