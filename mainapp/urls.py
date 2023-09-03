from django.contrib import admin
from django.urls import path
from mainapp.views import *

app_name = 'mainapp'

urlpatterns = [
    path('endpages/<str:status>', redirectPageView.as_view()),    
    path('login', signin, name="signin"),
    path('signout', signout, name="signout"),
    path('dashboard', projectlistView.as_view(), name="projectlist"),
    path('delete/<pk>', deleteEntry.as_view(), name="deleteentry"),
    path('userlist', allUserList.as_view(), name="userlist"),
    path('user/resetpassword/', changePassword.as_view(), name="changePassword"),
]
