# models.py
from django.db import models
from Workers.models import AccountType
from Students.models import Students


class Overhead(models.Model):
    name = models.CharField(max_length=255)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    payed = models.IntegerField()
    date = models.DateTimeField()


class DeleteDOverhead(models.Model):
    over_head = models.ForeignKey(Overhead, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField()


class StudentMonthPayments(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    class_price = models.IntegerField()
    payed = models.IntegerField()
    another = models.IntegerField()
    month = models.DateTimeField()
    real_price = models.IntegerField()
    discount_percentage = models.IntegerField()


class StudentPaymentsInMonth(models.Model):
    student_month_payments = models.ForeignKey(StudentMonthPayments, on_delete=models.CASCADE,
                                               related_name='student_payments_in_month')
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    payed = models.IntegerField()
    date = models.DateTimeField()


class DiscountType(models.Model):
    name = models.CharField(max_length=255)


class StudentDiscount(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='student_discount')
    discount_type = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    discount_percentage = models.IntegerField()
