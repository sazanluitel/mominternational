from django.urls import path
from dashboard.views.pages import *
from dashboard.views.event import *

app_name = "dashboard"

urlpatterns = [
    path('admin/',DashboardView.as_view(), name='index'),
    path('add',AddView.as_view(), name='add'),
    path('list',pagelistview.as_view(), name='list'),
    path('pageajax',PagesAjaxView.as_view(), name='pageajax'),
    # path('addpost',AddpostView.as_view(), name='addpost'),
    # path('postview',PostView.as_view(), name='postview'),
    path('eventajax',EventAjaxView.as_view(), name='eventajax'),
    path('eventAdd',AddEventView.as_view(), name='addEvent'),
    path('eventView',EventView.as_view(), name='eventview'),
    path('eventajaxview',CourseAjaxView.as_view(), name='courseajaxview'),
    path('adduser',Adduser.as_view(), name='adduser'),
    path('userlist',UserList.as_view(), name='userlist'),
    path('usersajax',UsersAjax.as_view(), name='usersajax'),
    path('settings',Settings.as_view(), name='settings'),

    path("page/add/", AddPagesView.as_view(), name="addpage"),
    path("pages/", PagesView.as_view(), name="pages"),
    path("pages/ajax/", PagesAjaxView.as_view(), name="pageajax"),
    path("page/edit/<id>/", EditPagesView.as_view(), name="editpage"),

    path("event/edit/<id>/", EditEventView.as_view(), name="editevent"),

]