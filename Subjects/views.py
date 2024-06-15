from rest_framework import generics
from rest_framework.permissions import *

from .models import Subjects
from .permissions import *
from .serializers import SubjectSerializer


class SubjectListView(generics.ListCreateAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
