from django.urls import path
from .views import FlowListCreateAPIView, FlowRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('flows/', FlowListCreateAPIView.as_view(), name='flow-list-create'),
    path('flows/<int:pk>/', FlowRetrieveUpdateDestroyAPIView.as_view(), name='flow-detail'),
]
