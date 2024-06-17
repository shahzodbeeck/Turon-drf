from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from Flow.models import *
from Students.models import *
from Subjects.serializers import SubjectSerializer
from Teachers.serializers import TeacherSerializer
from Vacations.models import *
from Vacations.serializers import InfoSerializer
from turon.permission import IsAdminOrReadOnly
from .serializers import ClassSerializer, ClassTypeSerializer
from Flow.serializers import LanguageTypeSerializer

class ClassesView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request):
        user = request.user
        about_us = Info.objects.filter(type_id=1).order_by('id').first()
        about_id = about_us.id if about_us else 0
        teachers = Teacher.objects.all()
        page = request.query_params.get('page', 1)
        students = Class.objects.filter(deleted_classes__isnull=True)
        pages = students.paginate(page=page, per_page=50)
        student_count = Class.objects.count()
        languages = LanguageType.objects.all()

        data = {
            'about_us': InfoSerializer(about_us).data,
            'about_id': about_id,
            'teachers': TeacherSerializer(teachers, many=True).data,
            'pages': pages,
            'student_count': student_count,
            'languages': LanguageTypeSerializer(languages, many=True).data,
        }

        return Response(data)


class FilterClassesView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get('info', {})
        filter_classes = []
        classes = Class.objects.filter(deleted_classes__isnull=True)

        if info['language_type'] != "all":
            classes = classes.filter(language_type=info['language_type'])

        if info['class_number'] != 'sinflar':
            classes = classes.filter(class_number=info['class_number'])

        for group in classes:
            if info['color'] == "all" or info['color'] == group.color:
                filtered = {
                    "id": group.id,
                    "name": group.name,
                    "teacher": group.teacher.first().user.name if group.teacher.exists() else '',
                    "student_number": group.student.count(),
                    "class_number": group.class_number,
                    "color": group.color,
                    "language": group.language.name
                }
                filter_classes.append(filtered)

        return Response({"filter_classes": filter_classes})


class CreateClassView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        class_info = request.data.get('class_info', {})
        class_name = class_info['name']
        class_number = class_info['class_number']
        class_color = class_info['color']
        language_type = class_info['creat_language_type']
        teacher_id = class_info['teacher_id']
        students = class_info['students']

        new_class = Class.objects.create(
            name=class_name,
            class_number=class_number,
            color=class_color,
            language_type=language_type
        )

        teacher = Teacher.objects.get(id=teacher_id)
        if not teacher.classes.exists():
            teacher.classes.add(new_class)
        else:
            return Response({"error": "Teacher already assigned to a class"}, status=status.HTTP_400_BAD_REQUEST)

        for student_id in students:
            student = Students.objects.get(user_id=student_id)
            if not student.classes.exists():
                student.classes.add(new_class)
            else:
                return Response({"error": f"Student {student_id} already assigned to a class"},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class ClassProfileView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, class_id):
        user = request.user
        class_instance = Class.objects.get(id=class_id)
        students_count = class_instance.student.count()
        teachers = Teacher.objects.filter(classes__isnull=True)
        about_us = Info.objects.filter(type_id=1).first()
        about_id = about_us.id if about_us else 0
        classes = Class.objects.all()
        class_types = ClassType.objects.order_by('id').all()

        data = {
            'class': ClassSerializer(class_instance).data,
            'students_count': students_count,
            'teachers': TeacherSerializer(teachers, many=True).data,
            'about_us': InfoSerializer(about_us).data,
            'about_id': about_id,
            'classes': ClassSerializer(classes, many=True).data,
            'class_types': ClassTypeSerializer(class_types, many=True).data,
        }

        return Response(data)


class EditClassView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request, class_id):
        group = Class.objects.get(id=class_id)
        name = request.data.get("name")
        teacher_id = request.data.get("teacher")
        color = request.data.get("color")
        class_number = request.data.get("class_number")

        group.name = name
        group.color = color
        group.class_number = class_number

        if teacher_id:
            new_teacher = Teacher.objects.get(id=teacher_id)
            if group.teacher.exists():
                old_teacher = group.teacher.first()
                group.teacher.remove(old_teacher)
                group.teacher.add(new_teacher)
            else:
                group.teacher.add(new_teacher)

        group.save()
        return Response(status=status.HTTP_200_OK)


class DeleteStudentInClassView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get("info", {})
        class_instance = Class.objects.get(id=info['class_id'])
        student = Students.objects.get(id=info['student_id'])
        delete_type = info["delete_type"]
        reason = info['reason']

        student.classes.remove(class_instance)

        if delete_type == "in_class":
            DeletedStudentForClasses.objects.create(student_id=student.id, class_id=class_instance.id, reason=reason)
        else:
            DeletedStudent.objects.create(student_id=student.id)
            DeletedStudentForClasses.objects.create(student_id=student.id, class_id=class_instance.id, reason=reason)

        return Response(status=status.HTTP_200_OK)


class TransferStudentsInClassView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get("info_class", {})
        new_class = Class.objects.get(id=info["class_id"])

        for student_id in info["students"]:
            student = Students.objects.get(id=student_id)
            old_class = student.classes.first()
            student.classes.remove(old_class)
            student.classes.add(new_class)

        return Response(status=status.HTTP_200_OK)


class DeleteClassView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get("info", {})
        class_instance = Class.objects.get(id=info['class_id'])
        delete_type = info["delete_type"]
        reason = info['reason']

        if class_instance.student.exists():
            for student in class_instance.student.all():
                student.classes.remove(class_instance)

                if delete_type == "in_class":
                    DeletedStudentForClasses.objects.create(student_id=student.id, class_id=class_instance.id,
                                                            reason=reason)
                else:
                    DeletedStudent.objects.create(student_id=student.id)
                    DeletedStudentForClasses.objects.create(student_id=student.id, class_id=class_instance.id,
                                                            reason=reason)

            DeletedClasses.objects.create(class_instance=class_instance)
        else:
            DeletedClasses.objects.create(class_instance=class_instance)

        class_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClassSubjectsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, class_id):
        user = request.user
        about_us = Info.objects.filter(type_id=1).first()
        news = Info.objects.filter(type_id=2).first()
        jobs = Info.objects.filter(type_id=3).first()
        about_id = about_us.id if about_us else 0
        class_instance = Class.objects.get(id=class_id)
        subjects = Subjects.objects.all()

        data = {
            'class': ClassSerializer(class_instance).data,
            'about_us': InfoSerializer(about_us).data,
            'news': InfoSerializer(news).data,
            'jobs': InfoSerializer(jobs).data,
            'about_id': about_id,
            'subjects': SubjectSerializer(subjects, many=True).data,
        }

        return Response(data)


class AddClassSubjectsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get("info", {})
        class_instance = Class.objects.get(id=int(info["class_id"]))

        for subject_id in info["subjects"]:
            subject = Subjects.objects.get(id=int(subject_id))
            class_instance.subjects.add(subject)

        if info["remove_subject"]:
            for subject_id in info["remove_subject"]:
                subject = Subjects.objects.get(id=int(subject_id))
                class_instance.subjects.remove(subject)

        return Response(status=status.HTTP_200_OK)
