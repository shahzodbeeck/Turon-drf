import datetime

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.response import Response

from Workers.serializers import AccountTypeSerializer
from .permissions import *
from .serializers import *


class RegisterTeacher(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = RegisterTeacherSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


    @action(detail=False, methods=['post'])
    def teacher_attendance(self, request):
        info = request.data["info"]
        teacher_id = info["teacher_id"]
        year_id = info["year_id"]
        month_id = info["month_id"]
        day_id = info["day_id"]
        status = info["status"]
        now_attendance = TeacherAttendance.objects.filter(
            teacher_id=teacher_id, year=year_id, month=month_id, day=day_id
        ).first()
        if not now_attendance:
            TeacherAttendance.objects.create(
                teacher_id=teacher_id, year=year_id, month=month_id, day=day_id, status=status
            )
            self.calculate_teacher_salary()
            return Response("keldi")
        else:
            return Response("bu kunda davomat qilingan")

    @action(detail=True, methods=['get'])
    def teacher_salary(self, request, pk=None):
        teacher = self.get_object()
        salaries = TeacherSalary.objects.filter(teacher_id=teacher.id)
        teacher_salary_types = TeacherSalaryType.objects.all()
        return Response({
            "salaries": TeacherSalarySerializer(salaries, many=True).data,
            "teacher": TeacherSerializer(teacher).data,
            "teacher_salary_types": TeacherSalaryTypeSerializer(teacher_salary_types, many=True).data
        })

    @action(detail=False, methods=['post'])
    def enter_teacher_salary_type(self, request):
        info = request.data["info"]
        teacher_id = info["teacher_id"]
        salary_type_id = info["salary_type_id"]
        Teacher.objects.filter(id=teacher_id).update(salary_type=salary_type_id)
        self.calculate_teacher_salary()
        return Response()

    @action(detail=False, methods=['post'])
    def create_teacher_salary_type(self, request):
        info = request.data["info"]
        teacher_id = info["teacher_id"]
        type_name = info["salary_type_name"]
        salary = info["new_salary_money"]
        new_salary_type = TeacherSalaryType.objects.create(type_name=type_name, salary=salary)
        Teacher.objects.filter(id=teacher_id).update(salary_type=new_salary_type.id)
        self.calculate_teacher_salary()
        return Response()

    @action(detail=True, methods=['post'])
    def add_teacher_salary_percentage(self, request, pk=None):
        salary_percentage = request.data.get("salary_percentage")
        Teacher.objects.filter(id=pk).update(salary_percentage=salary_percentage)
        return Response()

    @action(detail=False, methods=['post'])
    def given_teacher_salary(self, request):
        info = request.data["info"]
        teacher_salary_id = info["teacher_salary_id"]
        account_type_id = info["account_type_id"]
        money = info["money"]
        reason = info["reason"]

        today = datetime.today()
        year = Years.objects.get(year=today.year)
        month = Month.objects.get(month_number=today.month, years_id=year.id)
        day = Day.objects.get(year_id=year.id, month_id=month.id, day_number=today.day)
        GivenSalariesInMonth.objects.create(
            given_salary=money, reason=reason, teacher_salary_id=teacher_salary_id,
            day_id=day.id, account_type_id=account_type_id, year_id=year.id, month_id=month.id
        )
        teacher_salary = TeacherSalary.objects.get(id=teacher_salary_id)
        old_given_salary = sum([salary.given_salary for salary in teacher_salary.given_salaries_in_month.all()])
        calc_salary = float(teacher_salary.salary) - float(old_given_salary)
        TeacherSalary.objects.filter(id=teacher_salary_id).update(
            rest_salary=round(calc_salary),
            give_salary=old_given_salary
        )
        return Response()

    @action(detail=False, methods=['post'])
    def delete_teacher_given_salary(self, request):
        info = request.data["info"]
        given_salary_id = info["given_salary_id"]
        GivenSalariesInMonth.objects.filter(id=given_salary_id).delete()
        return Response()

    @action(detail=True, methods=['get'])
    def teacher_salaries_in_month(self, request, pk=None):
        teacher_salary = TeacherSalary.objects.get(id=pk)
        account_types = AccountType.objects.all()
        return Response({
            "teacher_salary": TeacherSalarySerializer(teacher_salary).data,
            "account_types": AccountTypeSerializer(account_types, many=True).data
        })

    @action(detail=False, methods=['post'])
    def enter_teacher_worked_days(self, request):
        info = request.data["info"]
        teacher_salary_id = info["teacher_salary_id"]
        worked_days = info["worked_days"]
        TeacherSalary.objects.filter(id=teacher_salary_id).update(worked_days=worked_days)
        self.calculate_teacher_salary()
        return Response()

    def calculate_teacher_salary(self):
        teachers = Teacher.objects.all()
        today = datetime.today()
        year = Years.objects.get(year=today.year)
        month = Month.objects.get(month_number=today.month, years_id=year.id)
        working_days = Day.objects.filter(month_id=month.id, type_id=1).count()

        for teacher in teachers:
            if teacher.daily_table:
                lesson_count = len(teacher.daily_table)
                salary_percentage = teacher.salary_percentage
                calc_salary = (lesson_count / 20) * teacher.teacher_salary_type.salary
                percentage_result = (calc_salary * salary_percentage) / 100

                salary = TeacherSalary.objects.filter(teacher_id=teacher.id, month=month.id).first()
                if salary and salary.worked_days:
                    overall = (calc_salary + percentage_result) * (salary.worked_days / working_days)
                    salary.salary = round(overall)
                else:
                    overall = calc_salary + percentage_result
                    TeacherSalary.objects.create(teacher_id=teacher.id, salary=round(overall), month=month.id)
            else:
                TeacherSalary.objects.filter(teacher_id=teacher.id, month=month.id).update(salary=0)
        return Response("hello")
