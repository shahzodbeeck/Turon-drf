from rest_framework import generics
from rest_framework.permissions import *

from turon.permission import IsAdminOrReadOnly
from .serializers import *


class CreateJobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class =JobSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class JobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
