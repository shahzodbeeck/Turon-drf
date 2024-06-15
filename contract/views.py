# contract/views.py

import datetime
import os
from urllib.parse import urljoin

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from docxtpl import DocxTemplate
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from Students.models import Students
from Vacations.models import TypeInfo, Info
from Vacations.serializers import TypeInfoSerializer, InfoSerializer
from .permissions import IsAdminOrReadOnly


class CreateContractView(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, student_id):
        student = get_object_or_404(Students, id=student_id)

        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=1)
        jobs = get_object_or_404(TypeInfo, id=1)
        about = Info.objects.filter(type_info_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0

        return Response({
            "about_us": TypeInfoSerializer(about_us).data,
            "news": TypeInfoSerializer(news).data,
            "jobs": TypeInfoSerializer(jobs).data,
            "about_id": about_id,
            "user": student.user.id,
            "student": student.id
        })

    def post(self, request, student_id):
        student = get_object_or_404(Students, id=student_id)

        document_path = os.path.join(os.path.dirname(__file__), "primary_shartnoma.docx")

        if not os.path.exists(document_path):
            return Response({"error": "Template file not found."}, status=status.HTTP_404_NOT_FOUND)

        doc = DocxTemplate(document_path)

        student_name = f'{student.user.first_name} {student.user.last_name}'
        print(student.user.first_name)
        name = request.data.get("name")
        surname = request.data.get("surname")
        father_name = request.data.get("parent_name")
        parent = f'{name} {surname} {father_name}'
        passport = request.data.get("passport_seria")
        location_get = request.data.get("get_location")
        today = datetime.datetime.today()
        location = request.data.get("address")

        context = {
            "NAME": student_name,
            "PARENT": parent,
            "PASSPORT": passport,
            "LOCATIONGET": location_get,
            "TODAY": today.strftime("%Y-%m-%d"),
            "LOCATION": location
        }

        doc.render(context)
        folder = os.path.join("static", "docx_contract")
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, f"{student.user.first_name} {student.user.last_name}-contract.docx")
        doc.save(file_path)
        file_url = urljoin(request.build_absolute_uri('/'), file_path.replace("\\", "/"))

        return Response({"file_url": file_url})


class DownloadView(views.APIView):
    def get(self, request, filename):
        file_path = os.path.join('static', filename)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
