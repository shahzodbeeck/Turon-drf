from rest_framework import generics
from rest_framework.permissions import *

from .permissions import *
from .serializers import *


class RegisterTeacher(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = RegisterTeacherSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        subject = self.request.query_params.get('subject')
        if subject == 'all':
            return queryset
        return queryset.filter(subject__name=subject)


class TeacherProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
