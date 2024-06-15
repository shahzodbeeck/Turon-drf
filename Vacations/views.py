from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import *

from .models import TypeInfo, Info, Vacation, Requests
from .permission import IsAdminOrReadOnly
from .serializers import TypeInfoSerializer, InfoSerializer, VacationSerializer, RequestsSerializer


class TypeInfoListCreate(generics.ListCreateAPIView):
    queryset = TypeInfo.objects.all()
    serializer_class = TypeInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class TypeInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TypeInfo.objects.all()
    serializer_class = TypeInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class InfoListCreate(generics.ListCreateAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class InfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class VacationListCreate(generics.ListCreateAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class VacationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class RequestsListCreate(generics.ListCreateAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class RequestsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


default_storage = 'images/pdf'


class RequestsListCreate(generics.ListCreateAPIView):
    queryset = Requests.objects.all()
    serializer_class = RequestsSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        if file:
            file_name = default_storage.save(file.name, file)
            file_url = default_storage.url(file_name)
            serializer.save(pdf_file=file_url)
        else:
            serializer.save()
