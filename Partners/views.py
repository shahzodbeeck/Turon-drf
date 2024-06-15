from rest_framework import generics
from rest_framework.permissions import *

from .permission import IsAdminOrReadOnly
from .serializers import *


class CreatePartnersList(generics.ListCreateAPIView):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class PartnersRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
