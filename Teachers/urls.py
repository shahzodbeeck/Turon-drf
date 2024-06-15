from django.urls import path
from .views import  *

urlpatterns = [
    path('register/', RegisterTeacher.as_view(), name='register_teacher'),
    path('teachers/', TeacherList.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', TeacherProfile.as_view(), name='teacher_profile'),
]