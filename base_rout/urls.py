from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfoViewSet, CommentsViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'info', InfoViewSet, basename='info')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
