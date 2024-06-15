from rest_framework import generics
from rest_framework.permissions import *

from .models import Flow
from .permission import IsAdminOrReadOnly
from .serializers import FlowSerializer


class FlowListCreateAPIView(generics.ListCreateAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class FlowRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
