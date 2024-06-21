# views.py
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import os
from werkzeug.utils import secure_filename

from Users.models import CustomUser as User
from account.models import StudentMonthPayments
from .models import *
from .models import Students as Student
from .permissions import IsAdminOrReadOnly
from .serializers import *
from .serializers import RegisterStudentSerializer, StudentSerializer, DeletedStudentSerializer, PdfContractSerializer


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


class NotInClassStudentView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(classes=None)


class JoinClassView(generics.UpdateAPIView):
    serializer_class = StudentSerializer

    def update(self, request, *args, **kwargs):
        join_class = request.data.get("join_class")
        group = get_object_or_404(Class, id=join_class['class_id'])
        students = join_class['students']

        month_list = []
        today = datetime.today()
        if today.month == 1:
            start = datetime(today.year, today.month, today.day)
            end = datetime(today.year, 5, 1)
        else:
            start = datetime(today.year, today.month, today.day)
            next_year = today.year + 1
            end = datetime(next_year, 5, 1)

        for delta in range((end - start).days + 1):
            result_date = start + timedelta(days=delta)
            months = f'{result_date.month}-1-{result_date.year}'
            if months not in month_list:
                month_list.append(months)

        for student_id in students:
            student = get_object_or_404(Student, user_id=int(student_id))
            student.classes.add(group)
            student.save()
            for month in month_list:
                data_object = datetime.strptime(month, '%m-1-%Y')
                StudentMonthPayments.objects.create(student_id=student.id, month=data_object)

        return Response(status=status.HTTP_204_NO_CONTENT)


class EditUserPasswordView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        info = request.data.get("info")
        user.set_password(info)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditUsernameView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        info = request.data.get("info")
        user.username = info
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OldStudentView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.exclude(classes=None)


class PdfContractView(generics.CreateAPIView):
    serializer_class = PdfContractSerializer

    def post(self, request, student_id, *args, **kwargs):
        pdf = request.FILES.get('pdf')
        folder = "static/pdf_contract/"
        if pdf and self.check_file(pdf.name):
            photo_file = secure_filename(pdf.name)
            photo_url = f'/{folder}{photo_file}'
            pdf_path = os.path.join(folder, photo_file)
            with open(pdf_path, 'wb+') as destination:
                for chunk in pdf.chunks():
                    destination.write(chunk)
            PdfContract.objects.create(user_id=student_id, pdf=photo_url)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def check_file(self, filename):
        allowed_extensions = ['pdf']
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


class SearchNotInClassStudentView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        search = self.request.data.get("search", "")
        return User.objects.filter(student__classes=None).filter(
            models.Q(name__icontains=search) | models.Q(surname__icontains=search)
        ).order_by('name')


class SearchInClassStudentView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        search = self.request.data.get("search", "")
        return User.objects.filter(student__classes__isnull=False).filter(
            models.Q(name__icontains=search) | models.Q(surname__icontains=search)
        ).order_by('name')


class DeleteStudentView(generics.DestroyAPIView):
    serializer_class = DeletedStudentSerializer

    def destroy(self, request, *args, **kwargs):
        student_id = request.data.get("id")
        DeletedStudent.objects.create(student_id=student_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeletedStudentsView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(deleted_student=True)


class ReturnStudentsView(generics.DestroyAPIView):
    serializer_class = DeletedStudentSerializer

    def destroy(self, request, *args, **kwargs):
        student_id = request.data.get("id")
        DeletedStudent.objects.filter(student_id=student_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FilterDeleteStudentView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        info = self.request.data.get("info", {})
        search = info.get("search", "")
        language_type = info.get("language_type", "all")
        class_number = info.get("class_number", "sinflar")
        from_age = int(info.get("from", 0))
        to_age = int(info.get("to", 100))
        current_year = datetime.now().year

        students = Student.objects.filter(deleted_student=True)
        if search:
            students = students.filter(
                models.Q(user__name__icontains=search) |
                models.Q(user__surname__icontains=search)
            )
        if language_type != "all":
            students = students.filter(language_type__name=language_type)
        if class_number != "sinflar":
            students = students.filter(class_number=class_number)
        students = students.annotate(
            age=current_year - models.F('user__birth_date__year')
        ).filter(age__gte=from_age, age__lte=to_age)
        return students


class SearchDeleteStudentView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        search = self.request.data.get("search", "")
        return User.objects.filter(student__deleted_student=True).filter(
            models.Q(name__icontains=search) | models.Q(surname__icontains=search)
        ).order_by('name')
