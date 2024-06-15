from rest_framework import serializers

from .models import Worker, WorkerSalary, WorkerSalaryInDay, DeletedWorkerSalaryInDay, AccountType


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'


class WorkerSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSalary
        fields = '__all__'


class WorkerSalaryInDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerSalaryInDay
        fields = '__all__'


class DeletedWorkerSalaryInDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedWorkerSalaryInDay
        fields = '__all__'
