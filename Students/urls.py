from django.urls import path
from .views import  *

urlpatterns = [
    path('register/', RegisterStudent.as_view(), name='register_student'),
    path('student/', StudentList.as_view(), name='student_list'),
    path('student/<int:pk>/', StudentProfile.as_view(), name='student_profile'),
]