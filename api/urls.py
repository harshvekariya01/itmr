from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [
    path('projectlist', ProjectListAPIView.as_view({'get':'list'}), name="api_projectlist"),
]
