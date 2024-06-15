from django.urls import path
from .views import *

urlpatterns = [
    path('galery/', CreateGaleryList.as_view(), name='galery-list-create'),
    path('galery/<int:pk>/', GaleryRetrieveUpdateDestroyAPIView.as_view(), name='galery-detail'),
]
