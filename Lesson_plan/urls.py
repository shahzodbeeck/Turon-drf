from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonPlanDayViewSet

router = DefaultRouter()
router.register(r'lesson_plan', LessonPlanDayViewSet, basename='lesson_plan')

urlpatterns = [
    path('', include(router.urls)),
]
