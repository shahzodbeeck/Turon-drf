from django.db import models

from Calendar.models import Day, Month, Years
from Subjects.models import Subjects
from Users.models import CustomUser
from Workers.models import AccountType


class TeacherSalaryType(models.Model):
    type_name = models.CharField(max_length=255)
    salary = models.IntegerField()

    def add(self):
        self.save()


class Teacher(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    salary_percentage = models.IntegerField(null=True)
    salary_type = models.ForeignKey(TeacherSalaryType, on_delete=models.CASCADE)

    def add(self):
        self.save()


class TeacherSalary(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    salary = models.CharField(max_length=255)
    give_salary = models.CharField(max_length=255)
    month_id = models.ForeignKey(Month, on_delete=models.CASCADE)
    rest_salary = models.CharField(max_length=255)
    worked_days = models.CharField(max_length=255)

    def add(self):
        self.save()


class GivenSalariesInMonth(models.Model):
    teacher_salary = models.ForeignKey(TeacherSalary, on_delete=models.CASCADE)
    given_salary = models.CharField(max_length=255)
    year_id = models.ForeignKey(Years, on_delete=models.CASCADE)
    month_id = models.ForeignKey(Month, on_delete=models.CASCADE)
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    reason = models.TextField()
    account_type_id = models.ForeignKey(AccountType, on_delete=models.CASCADE)

    def add(self):
        self.save()


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year_id = models.ForeignKey(Years, on_delete=models.CASCADE)
    month_id = models.ForeignKey(Month, on_delete=models.CASCADE)
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    status = models.BooleanField()

    def add(self):
        self.save()


class Teacher_salary_day(models.Model):
    salary = models.IntegerField()
    reason = models.TextField()
    account_type_id = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    day_id = models.ForeignKey(Day, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    teacher_salary = models.ForeignKey(TeacherSalary, on_delete=models.CASCADE)

    def add(self):
        self.save()


class DeletedTeacherSalaryInDay(models.Model):
    teacher_salary_day = models.ForeignKey(Teacher_salary_day, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add(self):
        self.save()
