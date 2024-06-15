from django.db import models

from Calendar.models import Day, Years, Month
from Jobs.models import Job
from Users.models import CustomUser




class Worker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='workers', on_delete=models.CASCADE)
    salary = models.CharField(max_length=255)


class WorkerSalary(models.Model):
    worker = models.ForeignKey(Worker, related_name='worker_salaries', on_delete=models.CASCADE)
    salary = models.CharField(max_length=255)
    give_salary = models.CharField(max_length=255)
    rest_salary = models.CharField(max_length=255)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)


class WorkerSalaryInDay(models.Model):
    salary = models.IntegerField()
    reason = models.CharField(max_length=255)
    account_type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    year = models.ForeignKey(Years, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    worker_salary = models.ForeignKey(WorkerSalary, related_name='worker_salary_in_days', on_delete=models.CASCADE)


class DeletedWorkerSalaryInDay(models.Model):
    worker_salary_in_day = models.ForeignKey(WorkerSalaryInDay, related_name='deleted_entries',
                                             on_delete=models.CASCADE)
    date = models.DateTimeField()


class AccountType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
