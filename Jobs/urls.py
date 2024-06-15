from django.urls import path

from .views import *

urlpatterns = [
    path('job/', CreateJobList.as_view(), name='job-list-create'),
    path('job/<int:pk>/', JobRetrieveUpdateDestroyAPIView.as_view(), name='job-detail'),
]
