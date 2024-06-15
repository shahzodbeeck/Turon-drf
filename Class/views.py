from rest_framework import generics
from rest_framework.permissions import *

from .models import ClassType, Class
from .permission import *
from .serializers import ClassTypeSerializer, ClassSerializer


class ClassTypeListCreateView(generics.ListCreateAPIView):
    queryset = ClassType.objects.all()
    serializer_class = ClassTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class ClassTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassType.objects.all()
    serializer_class = ClassTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class ClassListCreateView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class ClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
