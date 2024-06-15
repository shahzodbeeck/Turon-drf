from django.urls import path
from .views import *

urlpatterns = [
    path('partners/', CreatePartnersList.as_view(), name='Partners-list-create'),
    path('partners/<int:pk>/', PartnersRetrieveUpdateDestroyAPIView.as_view(), name='Partners-detail'),
]
