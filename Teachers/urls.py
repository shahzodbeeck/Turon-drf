from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)

urlpatterns = [
    path('register/', RegisterTeacher.as_view(), name='register_teacher'),
    path('', include(router.urls)),

]
