from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from Users.serializers import *
from Vacations.serializers import *
from turon.permission import IsAdminOrReadOnly
from .serializers import *


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    @action(detail=False, methods=['get'], url_path='home')
    def home(self, request):
        user = request.user
        news = Info.objects.filter(type_id=2).order_by('-id')[:3]
        about_us = Info.objects.filter(type_id=1).order_by('id').first()
        about_id = about_us.id if about_us else 0
        data = {
            'news': InfoSerializer(news, many=True).data,
            'about_id': about_id,
            'about_us': InfoSerializer(about_us).data,
            'user': CustomUserSerializer(user).data
        }
        return Response(data)

    @action(detail=False, methods=['get'], url_path='education')
    def education(self, request):
        user = request.user
        news = Info.objects.filter(type_id=2).order_by('-id')[:3]
        about_us = Info.objects.filter(type_id=1).order_by('id').first()
        about_id = about_us.id if about_us else 0
        data = {
            'news': InfoSerializer(news, many=True).data,
            'about_id': about_id,
            'about_us': InfoSerializer(about_us).data,
            'user': CustomUserSerializer(user).data
        }
        return Response(data)

    @action(detail=False, methods=['get'], url_path='time_table')
    def time_table(self, request):
        user = request.user
        news = Info.objects.filter(type_id=2).order_by('-id')[:3]
        about_us = Info.objects.filter(type_id=1).order_by('id').first()
        about_id = about_us.id if about_us else 0
        data = {
            'news': InfoSerializer(news, many=True).data,
            'about_id': about_id,
            'about_us': InfoSerializer(about_us).data,
            'user': CustomUserSerializer(user).data
        }
        return Response(data)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    @action(detail=False, methods=['post'], url_path='add_comment')
    def add_comment(self, request):
        text = request.data.get('text')
        comment = Comments(text=text, add_date=timezone.now())
        comment.save()
        return Response(status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(CustomUser, id=pk)
        if user.birth_date:
            birth_year = user.birth_date
            current_year = timezone.now().year
            age = current_year - birth_year.year
            user.age = age
            user.save()
        about_us = TypeInfo.objects.filter(id=1).first()
        news = TypeInfo.objects.filter(id=2).first()
        jobs = TypeInfo.objects.filter(id=3).first()
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first() if about_us else None
        about_id = about.id if about else 0
        data = {
            'user': CustomUserSerializer(user).data,
            'about_us': TypeInfoSerializer(about_us).data,
            'news': TypeInfoSerializer(news).data,
            'jobs': TypeInfoSerializer(jobs).data,
            'about': InfoSerializer(about).data,
            'about_id': about_id
        }
        return Response(data)
