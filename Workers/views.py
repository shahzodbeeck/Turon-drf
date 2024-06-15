from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from Jobs.serializers import JobSerializers
from turon.permission import IsAdminOrReadOnly
from .models import Worker, WorkerSalary, WorkerSalaryInDay, DeletedWorkerSalaryInDay, Job, CustomUser, Day, Years, \
    Month,AccountType
from .serializers import WorkerSerializer, WorkerSalarySerializer, WorkerSalaryInDaySerializer, \
    DeletedWorkerSalaryInDaySerializer,AccountTypeSerializer

class AccountTypeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

class WorkerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerSalaryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = WorkerSalary.objects.all()
    serializer_class = WorkerSalarySerializer


class WorkerSalaryInDayViewSet(viewsets.ModelViewSet):
    queryset = WorkerSalaryInDay.objects.all()
    serializer_class = WorkerSalaryInDaySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class DeletedWorkerSalaryInDayViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = DeletedWorkerSalaryInDay.objects.all()
    serializer_class = DeletedWorkerSalaryInDaySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def get_worker_salary(request):
    today = timezone.now()
    year = Years.objects.filter(year=today.year).first()
    month = Month.objects.filter(month_number=today.month, year=year).first()
    workers = Worker.objects.all()
    for worker in workers:
        if worker.salary:
            worker_salary = WorkerSalary.objects.filter(worker=worker, month=month).first()
            if not worker_salary:
                WorkerSalary.objects.create(worker=worker, salary=worker.salary, month=month)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def worker(request):
    get_worker_salary(request)
    workers = Worker.objects.all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def worker_profile(request, worker_id):
    worker = Worker.objects.filter(id=worker_id).first()
    if not worker:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = WorkerSerializer(worker)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def worker_salary_detail(request, worker_id):
    worker_salaries = WorkerSalary.objects.filter(worker_id=worker_id).order_by('id')
    serializer = WorkerSalarySerializer(worker_salaries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def worker_salaries_in_month(request, worker_salary_id):
    worker_salary = WorkerSalary.objects.filter(id=worker_salary_id).first()
    if not worker_salary:
        return Response(status=status.HTTP_404_NOT_FOUND)
    worker_salaries_in_day = WorkerSalaryInDay.objects.filter(worker_salary=worker_salary,
                                                              deleted_worker_salary_in_day__isnull=True).order_by('id')
    serializer = WorkerSalaryInDaySerializer(worker_salaries_in_day, many=True)
    return Response({
        'worker_salary': WorkerSalarySerializer(worker_salary).data,
        'worker_salaries_in_day': serializer.data,
        'account_types': AccountType.objects.all().values()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def change_worker_salary_account_type(request):
    info = request.data.get('info')
    worker_salary_in_day_id = info['worker_salary_in_day_id']
    account_type_id = info['account_type_id']
    WorkerSalaryInDay.objects.filter(id=worker_salary_in_day_id).update(account_type_id=account_type_id)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def given_worker_salary(request):
    info = request.data.get('info')
    worker_salary_id = info['worker_salary_id']
    account_type_id = info['account_type_id']
    money = info['money']
    reason = info['reason']
    today = timezone.now()
    year = Years.objects.filter(year=today.year).first()
    month = Month.objects.filter(month_number=today.month, year=year).first()
    day = Day.objects.filter(year=year, month=month, day_number=today.day).first()

    new_worker_salary_in_day = WorkerSalaryInDay.objects.create(
        salary=money, reason=reason, worker_salary_id=worker_salary_id,
        account_type_id=account_type_id, day_id=day.id, year_id=year.id, month_id=month.id
    )

    worker_salary = WorkerSalary.objects.filter(id=worker_salary_id).first()
    old_given_salary = sum(
        [int(s.salary) for s in worker_salary.worker_salary_in_days.filter(deleted_worker_salary_in_day__isnull=True)])
    calc_salary = float(worker_salary.salary) - old_given_salary
    worker_salary.give_salary = old_given_salary
    worker_salary.rest_salary = round(calc_salary)
    worker_salary.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def set_worker_salary(request):
    info = request.data.get('info')
    worker_id = info['worker_id']
    salary = info['new_salary_money']
    Worker.objects.filter(id=worker_id).update(salary=salary)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_worker_given_salary(request):
    info = request.data.get('info')
    given_salary_id = info['given_salary_id']
    today = timezone.now()
    date = timezone.now()
    deletes = WorkerSalaryInDay.objects.filter(id=given_salary_id).first()
    worker_salary = WorkerSalary.objects.filter(id=deletes.worker_salary_id).first()
    old_deleted_salary = int(worker_salary.give_salary) - int(deletes.salary)
    calc_salary = float(deletes.salary) + float(worker_salary.rest_salary)
    worker_salary.rest_salary = round(calc_salary)
    worker_salary.give_salary = old_deleted_salary
    worker_salary.save()
    DeletedWorkerSalaryInDay.objects.create(worker_salary_in_day_id=given_salary_id, date=date)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def register_worker(request):
    if request.method == 'POST':
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'first_name': request.data.get('name'),
            'last_name': request.data.get('surname'),
        }
        user = CustomUser.objects.create_user(**user_data)
        worker_data = {
            'user': user,
            'job_id': request.data.get('work_id'),
            'salary': request.data.get('salary', ''),
        }
        Worker.objects.create(**worker_data)
        return Response(status=status.HTTP_201_CREATED)
    else:
        jobs = Job.objects.all()
        return Response({'jobs': JobSerializers(jobs, many=True).data})
