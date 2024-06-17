# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from Users.serializers import CustomUserSerializer
from Vacations.models import *
from Vacations.serializers import InfoSerializer, TypeInfoSerializer
from turon.permission import IsAdminOrReadOnly


class AboutFrontView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    serializer_class = InfoSerializer

    def get(self, request, type_id, info_id, *args, **kwargs):
        if info_id == 0:
            info_id = None
        infos = Info.objects.filter(type_id=type_id).order_by('id').all()
        current_info = Info.objects.filter(id=info_id).order_by('id').first()
        about_us = Info.objects.filter(type_id=1).order_by('id').first()
        about_id = about_us.id if about_us else 0

        data = {
            'current_info': InfoSerializer(current_info).data,
            'infos': InfoSerializer(infos, many=True).data,
            'about_id': about_id
        }
        return JsonResponse(data)


class GetAboutProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    serializer_class = InfoSerializer

    def get(self, request, type_id, info_id, *args, **kwargs):
        user = request.user
        if not user:
            return redirect('home')
        if info_id == 0:
            info_id = None
        infos = Info.objects.filter(type_id=type_id).order_by('id').all()
        current_info = Info.objects.filter(id=info_id).order_by('id').first()
        about_us = TypeInfo.objects.filter(id=1).first()
        news = TypeInfo.objects.filter(id=2).first()
        jobs = TypeInfo.objects.filter(id=3).first()
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0

        data = {
            'type_id': type_id,
            'infos': InfoSerializer(infos, many=True).data,
            'current_info': InfoSerializer(current_info).data,
            'news': TypeInfoSerializer(news).data,
            'about_us': TypeInfoSerializer(about_us).data,
            'about_id': about_id,
            'jobs': TypeInfoSerializer(jobs).data,
            'user': CustomUserSerializer(user).data
        }
        return JsonResponse(data)

    def post(self, request, type_id, info_id, *args, **kwargs):
        title = request.data.get('title')
        text = request.data.get('text')
        img = request.FILES.get('img')
        add_info = Info(title=title, text=text, img=img, type_id=type_id)
        add_info.save()
        return redirect('get_about_profile', type_id=type_id, info_id=add_info.id)


class InfosView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    serializer_class = InfoSerializer

    def get(self, request, type_id, *args, **kwargs):
        user = request.user
        if not user:
            return redirect('home')
        jobs_list = Info.objects.filter(type_id=type_id).order_by('id').all()
        about_us = TypeInfo.objects.filter(id=1).first()
        news = TypeInfo.objects.filter(id=2).first()
        jobs = TypeInfo.objects.filter(id=3).first()
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0

        data = {
            'jobs_list': InfoSerializer(jobs_list, many=True).data,
            'type_id': type_id,
            'news': TypeInfoSerializer(news).data,
            'jobs': TypeInfoSerializer(jobs).data,
            'about_id': about_id,
            'about_us': TypeInfoSerializer(about_us).data,
            'user': CustomUserSerializer(user).data
        }
        return JsonResponse(data)

    def post(self, request, type_id, *args, **kwargs):
        title = request.data.get('title')
        text = request.data.get('text')
        img = request.FILES.get('img')

        add_info = Info(title=title, text=text, img=img, type_id=type_id)
        add_info.save()
        return redirect('infos', type_id=type_id)


class EditInfoView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    serializer_class = InfoSerializer

    def post(self, request, info_id, *args, **kwargs):
        user = request.user
        if not user:
            return redirect('home')

        title = request.data.get('title')
        text = request.data.get('text')
        img = request.FILES.get('img')

        info = get_object_or_404(Info, id=info_id)

        info.img = img

        info.title = title
        info.text = text
        info.save()

        if info.type_id == 1:
            return redirect('get_about_profile', type_id=info.type_id, info_id=info_id)
        elif info.type_id == 3:
            return redirect('infos', type_id=info.type_id)


class DeleteInfoView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    serializer_class = InfoSerializer

    def delete(self, request, info_id, *args, **kwargs):
        user = request.user
        if not user:
            return redirect('home')

        info = get_object_or_404(Info, id=info_id)
        type_id = info.type_id
        info.delete()

        get_info = Info.objects.order_by('id').first()
        if type_id == 1:
            if get_info:
                return redirect('get_about_profile', type_id=type_id, info_id=get_info.id)
            else:
                return redirect('get_about_profile', type_id=type_id, info_id=0)
        elif type_id == 3:
            return redirect('infos', type_id=type_id)
