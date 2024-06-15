# your_app_name/views.py

import datetime
import os

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from docxtpl import DocxTemplate
from rest_framework import views, status
from rest_framework.response import Response

from Students.models import Students
from Vacations.models import TypeInfo, Info


class CreateContractView(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, student_id):

        student = get_object_or_404(Students, id=student_id)


        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        about_id = about.id if about else 0

        return Response({
            "about_us": about_us,
            "news": news,
            "jobs": jobs,
            "about_id": about_id,
            "user": user,
            "student": student
        })

    def post(self, request, student_id):
        # error = self.check_session(request)
        # if error:
        #     return redirect('home')
        # user = self.current_user(request)
        student = get_object_or_404(Students, id=student_id)

        document_path = os.path.join(os.path.dirname(__file__), "primary_shartnoma.docx")
        doc = DocxTemplate(document_path)

        student_name = f'{student.name} {student.surname}'
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
        file_path = os.path.join(folder, f"{student.name} {student.surname}-contract.docx")
        doc.save(file_path)

        return Response({"file_url": request.build_absolute_uri(f"/{file_path}")})


class DownloadView(views.APIView):
    def get(self, request, filename):
        file_path = os.path.join('static', filename)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
