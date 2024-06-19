# serializers.py
from rest_framework import serializers
from .models import Overhead, StudentPaymentsInMonth, DeleteDOverhead, DiscountType, StudentDiscount, \
    StudentMonthPayments


class OverheadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overhead
        fields = ['id', 'name', 'account_type', 'payed', 'date']


class StudentPaymentsInMonthSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.name', read_only=True)
    student_surname = serializers.CharField(source='student.user.surname', read_only=True)
    account_type_name = serializers.CharField(source='account_type.name', read_only=True)

    class Meta:
        model = StudentPaymentsInMonth
        fields = ['id', 'student_id', 'student_name', 'student_surname', 'account_type_id', 'account_type_name',
                  'payed', 'date']


class DeleteDOverheadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteDOverhead
        fields = ['id', 'over_head_id', 'date']


class DiscountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountType
        fields = ['id', 'name']


class StudentDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDiscount
        fields = ['id', 'student_id', 'discount_type_id', 'discount_percentage']


class StudentMonthPaymentsSerializer(serializers.ModelSerializer):
    student_payments_in_month = StudentPaymentsInMonthSerializer(many=True, read_only=True)

    class Meta:
        model = StudentMonthPayments
        fields = ['id', 'student_id', 'account_type_id', 'class_price', 'payed', 'another', 'month', 'real_price',
                  'discount_percentage', 'student_payments_in_month']
