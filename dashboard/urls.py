from django.urls import path
from dashboard.views.pages import *
from dashboard.views.event import *

app_name = "dashboard"

urlpatterns = [
    path('admin/',DashboardView.as_view(), name='index'),
    
    path('eventajax',EventAjaxView.as_view(), name='eventajax'),
    path('event/add/',AddEventView.as_view(), name='addEvent'),
    path('events',EventView.as_view(), name='eventView'),
    path("event/edit/<id>/", EditEventView.as_view(), name="editevent"),



    path('adduser',Adduser.as_view(), name='adduser'),
    path('userlist',UserList.as_view(), name='userlist'),
    path('usersajax',UsersAjax.as_view(), name='usersajax'),

    path('settings',Settings.as_view(), name='settings'),

    path("page/add/", AddPagesView.as_view(), name="addpage"),
    path("pages/", PagesView.as_view(), name="pages"),
    path("pages/ajax/", PagesAjaxView.as_view(), name="pageajax"),
    path("page/edit/<id>/", EditPagesView.as_view(), name="editpage"),


]