# urls.py
from django.urls import path
from .views import (
    ClassTypeListCreateView,
    ClassTypeRetrieveUpdateDestroyView,
    ClassListCreateView,
    ClassRetrieveUpdateDestroyView
)

urlpatterns = [
    path('class-types/', ClassTypeListCreateView.as_view(), name='class-type-list-create'),
    path('class-types/<int:pk>/', ClassTypeRetrieveUpdateDestroyView.as_view(), name='class-type-detail'),
    path('classes/', ClassListCreateView.as_view(), name='class-list-create'),
    path('classes/<int:pk>/', ClassRetrieveUpdateDestroyView.as_view(), name='class-detail'),
]
