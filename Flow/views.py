from datetime import datetime

from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from Class.models import ClassType
from Class.serializers import ClassTypeSerializer
from Subjects.serializers import SubjectSerializer
from Teachers.serializers import TeacherSerializer
from Vacations.models import Info
from Vacations.serializers import InfoSerializer
from .models import Teacher, Students, Flow, LanguageType, Subjects
from .permission import *
from .serializers import StudentSerializer, FlowSerializer, LanguageTypeSerializer


class FlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request):
        user = request.user
        about_us = Info.objects.filter(type_id=1).first()
        teachers = Teacher.objects.all()
        students = Students.objects.filter(classes__isnull=False, deleted_student=False)
        flows = Flow.objects.all()
        languages = LanguageType.objects.all()
        subjects = Subjects.objects.all()

        data = {
            'about_us': InfoSerializer(about_us).data,
            'teachers': TeacherSerializer(teachers, many=True).data,
            'students': StudentSerializer(students, many=True).data,
            'flows': FlowSerializer(flows, many=True).data,
            'languages': LanguageTypeSerializer(languages, many=True).data,
            'subjects': SubjectSerializer(subjects, many=True).data
        }

        return Response(data)


class FilterStudentForFlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get('info', {})
        filtered_students = []
        students = Students.objects.filter(classes__isnull=False, deleted_student=False)

        for student in students:
            user = student.user
            birth_year = user.date_of_birth.year
            current_year = datetime.now().year
            age = current_year - birth_year

            if age >= int(info['from']) and age <= int(info['to']):
                filtered_students.append({
                    'id': user.id,
                    'username': user.username,
                    'name': user.first_name,
                    'birth_date': user.date_of_birth,
                    'number': user.profile.phone_number,  # Assuming there is a profile model with phone number
                    'image': user.profile.image.url,  # Assuming there is a profile model with image
                    'surname': user.last_name,
                    'age': age,
                    'language': student.language.name
                })

        return Response({'filter_student': filtered_students})


class CreateFlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        flow_info = request.data.get('flow_info', {})
        flow = Flow.objects.create(
            name=flow_info['name'],
            subject_id=flow_info['subject_id'],
            teacher_id=flow_info['teacher_id']
        )
        students = flow_info.get('students', [])
        for student_id in students:
            student = Students.objects.get(user_id=student_id)
            flow.students.add(student)

        flow.save()
        return Response(status=status.HTTP_201_CREATED)


class JoinFlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        join_class = request.data.get('join_class', {})
        flow = Flow.objects.get(id=join_class['class_id'])
        students = join_class.get('students', [])
        for student_id in students:
            student = Students.objects.get(user_id=student_id)
            flow.students.add(student)

        flow.save()
        return Response(status=status.HTTP_200_OK)


class FlowProfileView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, flow_id):
        flow = Flow.objects.get(id=flow_id)
        teachers = Teacher.objects.all()
        about_us = Info.objects.filter(type_id=1).first()
        students_count = flow.students.count()
        class_types = ClassType.objects.all()

        data = {
            'flow': FlowSerializer(flow).data,
            'students_count': students_count,
            'teachers': TeacherSerializer(teachers, many=True).data,
            'about_us': InfoSerializer(about_us).data,
            'class_types': ClassTypeSerializer(class_types, many=True).data
        }

        return Response(data)


class TransferStudentsInFlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get('info_flow', {})
        old_flow = Flow.objects.get(id=info['old_flow_id'])
        new_flow = Flow.objects.get(id=info['flow_id'])
        student_ids = info.get('students', [])

        for student_id in student_ids:
            student = Students.objects.get(id=student_id)
            old_flow.students.remove(student)
            new_flow.students.add(student)

        old_flow.save()
        new_flow.save()
        return Response(status=status.HTTP_200_OK)


class DeleteStudentInFlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get('info', {})
        flow = Flow.objects.get(id=info['flow_id'])
        student = Students.objects.get(id=info['student_id'])
        flow.students.remove(student)
        flow.save()
        return Response(status=status.HTTP_200_OK)


class DeleteFlowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get('info', {})
        flow = Flow.objects.get(id=info['flow_id'])
        flow.students.clear()
        flow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
