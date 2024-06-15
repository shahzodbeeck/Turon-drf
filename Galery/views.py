from rest_framework import generics
from rest_framework.permissions import *

from .permission import IsAdminOrReadOnly
from .serializers import *


class CreateGaleryList(generics.ListCreateAPIView):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class GaleryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
