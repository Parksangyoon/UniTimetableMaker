import django.conf.urls as urls

from scheduler.views.home_v import CompanyFormView, CompanyUpdateView
from scheduler.views.classroom_v import ClassroomListView, update_classroom, set_classroom
from scheduler.views.subject_v import SubjectListView, update_subject, set_subject
from scheduler.views.timetable_v import TimetableListView, update_timetable

urlpatterns = [
    urls.url(r'^$', CompanyFormView.as_view(), name='home'),
    urls.url(r'^edit_company/(?P<company_id>\d+)/$', CompanyUpdateView.as_view(), name='edit_company'),
    urls.url(r'^classroom/(?P<company_id>\d+)/$', ClassroomListView.as_view(), name='classroom_list'),
    urls.url(r'^classroom/update/(?P<company_id>\d+)/$', update_classroom, name='update_classroom'),
    urls.url(r'^classroom/set_range/(?P<company_id>\d+)/$', set_classroom, name='set_classroom_range'),
    urls.url(r'^subject/(?P<company_id>\d+)/$', SubjectListView.as_view(), name='subject_list'),
    urls.url(r'^subject/update/(?P<company_id>\d+)/$', update_subject, name='update_subject'),
    urls.url(r'^subject/setting/(?P<company_id>\d+)/$', set_subject, name='set_subject'),
    urls.url(r'^timetable/(?P<company_id>\d+)/$', TimetableListView.as_view(), name='timetable'),
    urls.url(r'^timetable/update/(?P<company_id>\d+)/$', update_timetable, name='set_timetable'),
]
