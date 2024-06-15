from django.urls import path
from . import views

urlpatterns = [

    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
]