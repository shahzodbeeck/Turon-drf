# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Students
from .permissions import IsAdminOrReadOnly
from .serializers import RegisterStudentSerializer, StudentSerializer


class RegisterStudent(generics.CreateAPIView):
    queryset = Students.objects.all()
    serializer_class = RegisterStudentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class StudentList(generics.ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class')
        if class_id and class_id != 'all':
            return queryset.filter(classs__id=class_id)
        return queryset


class StudentProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
