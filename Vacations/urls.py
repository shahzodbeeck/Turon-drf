from django.urls import path
from . import views

urlpatterns = [
    path('typeinfo/', views.TypeInfoListCreate.as_view(), name='typeinfo-list-create'),
    path('typeinfo/<int:pk>/', views.TypeInfoDetail.as_view(), name='typeinfo-detail'),
    path('info/', views.InfoListCreate.as_view(), name='info-list-create'),
    path('info/<int:pk>/', views.InfoDetail.as_view(), name='info-detail'),
    path('vacation/', views.VacationListCreate.as_view(), name='vacation-list-create'),
    path('vacation/<int:pk>/', views.VacationDetail.as_view(), name='vacation-detail'),
    path('requests/', views.RequestsListCreate.as_view(), name='requests-list-create'),
    path('requests/<int:pk>/', views.RequestsDetail.as_view(), name='requests-detail'),
]
