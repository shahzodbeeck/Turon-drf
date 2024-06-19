from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from .models import Overhead, StudentPaymentsInMonth, StudentMonthPayments, DiscountType, StudentDiscount, \
    DeleteDOverhead
from .serializers import OverheadSerializer, StudentPaymentsInMonthSerializer
from Vacations.models import Info, TypeInfo
from Users.models import CustomUser as User
from Students.models import Students as Student
import datetime
import string

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from Teachers.models import Teacher_salary_day as TeacherSalaryDay, Day
from Teachers.serializers import *
from Workers.serializers import *
from turon.permission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CollectionView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request):
        user = get_object_or_404(User, id=1)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        payments = StudentPaymentsInMonth.objects.all().order_by('id')
        cost_all = Overhead.objects.all().order_by('id')

        balance = sum(payment.payed for payment in payments)

        response_data = {
            'payments': StudentPaymentsInMonthSerializer(payments, many=True).data,
            'cost_all': OverheadSerializer(cost_all, many=True).data,
            'user': user,
            'about_us': about_us,
            'about_id': 0,
            'news': news,
            'jobs': jobs,
            'about': about,
            'balance': balance
        }

        return Response(response_data)


class SearchView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        input_one = request.data.get("input_one")
        input_two = request.data.get("input_two")
        button = request.data.get("button")
        button_number = 0

        if button == 'Bank':
            button_number = 1
        elif button == 'Click':
            button_number = 2
        elif button == 'Cash':
            button_number = 3

        payment_all = StudentPaymentsInMonth.objects.all().order_by('id')
        cost_all = Overhead.objects.all().order_by('id')
        list_pay = []
        list_cost = []

        def filter_records(records):
            filtered = []
            for record in records:
                if (
                        (button_number == 0 or record.account_type_id == button_number) and
                        input_one <= record.date.strftime("%Y-%m-%d") <= input_two
                ):
                    filtered.append(record.id)
            return filtered

        list_pay = filter_records(payment_all)
        list_cost = filter_records(cost_all)

        payments = StudentPaymentsInMonth.objects.filter(id__in=list_pay).order_by('id')
        cost_all_filter = Overhead.objects.filter(id__in=list_cost).order_by('id')

        list_pay_fetch = StudentPaymentsInMonthSerializer(payments, many=True).data
        list_cost_fetch = OverheadSerializer(cost_all_filter, many=True).data

        balance = sum(payment.payed for payment in payments) - sum(cost.payed for cost in cost_all_filter)

        return Response({
            'payments': list_pay_fetch,
            'cost': list_cost_fetch,
            'balance': balance
        })


class AddPaymentView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, student_id):
        today = datetime.today()
        user = request.user
        student = get_object_or_404(Student, id=student_id)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        account_types = AccountType.objects.all()
        return Response({
            'user': user,
            'about_us': about_us,
            'news': news,
            'jobs': jobs,
            'about': about,
            'account_types': account_types,
            'student': student
        })

    def post(self, request, student_id):
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        info = request.data.get("info")
        student_id = info["student_id"]
        money = info["money"]
        account_type_id = info["account_type_id"]
        student_mont_payments = StudentMonthPayments.objects.filter(student_id=student_id, another__gt=0).order_by(
            'id').all()
        get_money = money
        for student_mont_payment in student_mont_payments:
            student = get_object_or_404(Student, id=student_mont_payment.student_id)
            if student.student_discount.exists():
                discount_percentage = student.student_discount.first().discount_percentage
                result = student_mont_payment.class_price / 100 * discount_percentage
                discounted_price = student_mont_payment.class_price - result
                StudentMonthPayments.objects.filter(student_id=student_mont_payment.student_id,
                                                    id=student_mont_payment.id,
                                                    another=student_mont_payment.class_price).update({
                    "class_price": discounted_price,
                    "another": discounted_price,
                    "real_price": student_mont_payment.class_price,
                    "discount_percentage": discount_percentage
                })
            if student_mont_payment.another < get_money:
                get_money -= student_mont_payment.another
                StudentMonthPayments.objects.filter(student_id=student_mont_payment.student_id,
                                                    id=student_mont_payment.id).update({
                    "payed": student_mont_payment.class_price,
                    "another": 0,
                    "account_type_id": account_type_id
                })
                add = StudentPaymentsInMonth(student_id=student_mont_payment.student_id,
                                             student_month_payments_id=student_mont_payment.id, payed=get_money,
                                             date=date, account_type_id=account_type_id)
                add.save()
            else:
                another = student_mont_payment.another - get_money
                StudentMonthPayments.objects.filter(student_id=student_mont_payment.student_id,
                                                    id=student_mont_payment.id, another__gt=0).update({
                    "payed": get_money + student_mont_payment.payed,
                    "another": another,
                    "account_type_id": account_type_id
                })
                add = StudentPaymentsInMonth(student_id=student_mont_payment.student_id,
                                             student_month_payments_id=student_mont_payment.id, payed=get_money,
                                             date=date, account_type_id=account_type_id)
                add.save()
                filtered_payed = StudentMonthPayments.objects.filter(student_id=student_mont_payment.student_id,
                                                                     id=student_mont_payment.id, another=0).first()
                if filtered_payed:
                    StudentMonthPayments.objects.filter(student_id=student_mont_payment.student_id,
                                                        id=student_mont_payment.id, another=0).update({
                        "payed": student_mont_payment.class_price
                    })
            break
        return Response(status=status.HTTP_200_OK)


class PaymentListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, student_id):
        user = request.user
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        student_payments = StudentMonthPayments.objects.filter(student_id=student_id).order_by('id').all()
        student = get_object_or_404(Student, id=student_id)
        return Response({
            'user': user,
            'about_us': about_us,
            'news': news,
            'jobs': jobs,
            'about': about,
            'student_payments': student_payments,
            'student': student
        })


class PaymentInMonthView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, month_payment_id):
        user = request.user
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        student_payments = StudentPaymentsInMonth.objects.filter(student_month_payments_id=month_payment_id).all()
        return Response({
            'user': user,
            'about_us': about_us,
            'news': news,
            'jobs': jobs,
            'about': about,
            'student_payments': student_payments
        })


class AddCostView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        name = string.capwords(request.data.get('name'))
        payed = int(request.data.get('payed').replace(" ", ""))
        account_type_id = request.data.get('account_type_id')
        if name and payed and account_type_id:
            new_cost = Overhead(name=name, account_type_id=account_type_id, payed=payed, date=date)
            new_cost.save()
        return redirect('all_payments', type_request='cost', page_num=1)


class AllPaymentsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, type_request, page_num):
        user = request.user
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        payments = StudentPaymentsInMonth.objects.all().order_by('id')
        balance, cash, bank, click = self.calc()
        if type_request == 'pay':
            payments = StudentPaymentsInMonth.objects.all().order_by('id')
        elif type_request == 'cost':
            payments = Overhead.objects.filter(deleted_over_head__isnull=True).order_by('id')
        elif type_request == 'salary_teacher':
            payments = Teacher_salary_day.objects.filter(deleted_teacher_salary_inDay__isnull=True).order_by('id')
        elif type_request == 'salary_worker':
            payments = WorkerSalaryInDay.objects.filter(deleted_worker_salary_inDay__isnull=True).order_by('id')
        return Response({
            'user': user,
            'about_us': about_us,
            'news': news,
            'jobs': jobs,
            'about': about,
            'payments': payments,
            'balance': balance,
            'cash': cash,
            'bank': bank,
            'click': click
        })

    def calc(self):
        balance = 0
        cash = 0
        bank = 0
        click = 0
        payments_in_pay = StudentPaymentsInMonth.objects.all().order_by('id')
        cash_payments_in_pay = StudentPaymentsInMonth.objects.filter(account_type_id=3).all()
        bank_payments_in_pay = StudentPaymentsInMonth.objects.filter(account_type_id=1).all()
        click_payments_in_pay = StudentPaymentsInMonth.objects.filter(account_type_id=2).all()
        payments_in_cost = Overhead.objects.filter(deleted_over_head__isnull=True).all()
        cash_payments_in_cost = Overhead.objects.filter(account_type_id=3, deleted_over_head__isnull=True).all()
        bank_payments_in_cost = Overhead.objects.filter(account_type_id=1, deleted_over_head__isnull=True).all()
        click_payments_in_cost = Overhead.objects.filter(account_type_id=2, deleted_over_head__isnull=True).all()
        for payment in payments_in_pay:
            balance += payment.payed
        for cash_payment in cash_payments_in_pay:
            cash += cash_payment.payed
        for bank_payment in bank_payments_in_pay:
            bank += bank_payment.payed
        for click_payment in click_payments_in_pay:
            click += click_payment.payed
        for payment in payments_in_cost:
            balance -= payment.payed
        for cash_payment in cash_payments_in_cost:
            cash -= cash_payment.payed
        for bank_payment in bank_payments_in_cost:
            bank -= bank_payment.payed
        for click_payment in click_payments_in_cost:
            click -= click_payment.payed
        return balance, cash, bank, click


class AddDiscountView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def get(self, request, student_id):
        user = request.user
        student = get_object_or_404(Student, id=student_id)
        about_us = get_object_or_404(TypeInfo, id=1)
        news = get_object_or_404(TypeInfo, id=2)
        jobs = get_object_or_404(TypeInfo, id=3)
        about = Info.objects.filter(type_id=about_us.id).order_by('id').first()
        discount_types = DiscountType.objects.all()
        return Response({
            'user': user,
            'about_us': about_us,
            'news': news,
            'jobs': jobs,
            'about': about,
            'discount_types': discount_types,
            'student': student
        })

    def post(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        discount_type_id = request.data.get("discount_type")
        percentage = request.data.get("percentage")
        if student.student_discount.exists():
            filter_discount = student.student_discount.filter(discount_type_id=discount_type_id).first()
            if filter_discount:
                filter_discount.update(discount_percentage=percentage)
            else:
                add = StudentDiscount(discount_type_id=discount_type_id, student_id=student_id,
                                      discount_percentage=percentage)
                add.save()
        else:
            add = StudentDiscount(discount_type_id=discount_type_id, student_id=student_id,
                                  discount_percentage=percentage)
            add.save()
        return Response(status=status.HTTP_200_OK)


class CheckDiscountView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        info = request.data.get("info")
        student = get_object_or_404(Student, id=info["student_id"])
        discount_percentage = 0
        if student.student_discount.filter(discount_type_id=info["discount_type"]).exists():
            discount_percentage = student.student_discount.filter(
                discount_type_id=info["discount_type"]).first().discount_percentage
        return Response({
            "percentage": discount_percentage
        })


class DeletePaymentView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        payment_id = request.data.get("id")
        student_payment_in_month = get_object_or_404(StudentPaymentsInMonth, id=payment_id)
        month_payment = get_object_or_404(StudentMonthPayments, id=student_payment_in_month.student_month_payments_id)
        student_payment_in_month.delete()
        all_payments = StudentPaymentsInMonth.objects.filter(student_month_payments_id=month_payment.id).all()
        sum_payed = sum(payment.payed for payment in all_payments)
        month_payment.payed = sum_payed
        month_payment.another = month_payment.class_price - sum_payed
        month_payment.save()
        return Response(status=status.HTTP_200_OK)


class DeleteCostView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        cost_id = request.data.get("id")
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        cost = get_object_or_404(Overhead, id=cost_id)
        deleted_cost = DeleteDOverhead(over_head_id=cost.id, date=date)
        deleted_cost.save()
        return Response(status=status.HTTP_200_OK)


class DeleteSalaryWorkerView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        worker_salary_id = request.data.get("id")
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        salary_worker = DeletedWorkerSalaryInDay(worker_salary_in_day_id=worker_salary_id, date=date)
        salary_worker.save()
        return Response(status=status.HTTP_200_OK)


class DeleteSalaryTeacherView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        teacher_salary_id = request.data.get("id")
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        salary_teacher = DeletedTeacherSalaryInDay(teacher_salary_day_id=teacher_salary_id, date=date)
        salary_teacher.save()
        return Response(status=status.HTTP_200_OK)


class SearchPayView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        search = string.capwords(request.data.get("search"))
        pays = Student.objects.filter(user__name__icontains=search, student_month_payments__isnull=False).order_by(
            'id').distinct()
        student_id_list = pays.values_list('id', flat=True)
        payments = StudentPaymentsInMonth.objects.filter(student_id__in=student_id_list).order_by('id').all()
        filtered_pay = StudentPaymentsInMonthSerializer(payments, many=True).data
        return Response({
            "filtered_pay": filtered_pay
        })


class SearchCostView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        search = string.capwords(request.data.get("search"))
        cost_all = Overhead.objects.filter(name__icontains=search, deleted_over_head__isnull=True).order_by('id').all()
        filtered_cost = OverheadSerializer(cost_all, many=True).data
        return Response({
            "filtered_cost": filtered_cost
        })


class FilterSalaryView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        button_id = request.data.get("button_id")
        type_r = request.data.get("type")
        filtered_salary = []

        if type_r == 'salary_teacher':
            salary_all = Teacher_salary_day.objects.filter(account_type_id=button_id,
                                                           deleted_teacher_salary_inDay__isnull=True).order_by(
                'id').all()
            for salary in salary_all:
                info = {
                    'teacher_name': salary.teacher.user.name,
                    'reason': salary.reason,
                    'salary': salary.salary,
                    'account_type': salary.account_type.name,
                    'date': f'{salary.day.years.year} - {salary.day.month.month_number} - {salary.day.day_number}'
                }
                filtered_salary.append(info)
        else:
            salary_all = WorkerSalaryInDay.objects.filter(account_type_id=button_id,
                                                          deleted_worker_salary_inDay__isnull=True).order_by('id').all()
            for salary in salary_all:
                info = {
                    'worker_name': salary.worker_salary.worker.user.name,
                    'worker_job': salary.worker_salary.worker.job.name,
                    'reason': salary.reason,
                    'salary': salary.salary,
                    'account_type': salary.account_type.name,
                    'date': f'{salary.day.years.year} - {salary.day.month.month_number} - {salary.day.day_number}'
                }
                filtered_salary.append(info)
        return Response({
            'filtered_salary': filtered_salary
        })


class FilterDateView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    def post(self, request):
        year = request.data.get("year")
        month = request.data.get("month")
        day = request.data.get("day")
        type_r = request.data.get("type")
        filtered_salary = []

        if type_r == 'salary_teacher':
            query = Q(deleted_teacher_salary_inDay__isnull=True)
            if year:
                query &= Q(day__year_id=year)
            if month:
                query &= Q(day__month_id=month)
            if day:
                query &= Q(day__id=day)

            salary_all = TeacherSalaryDay.objects.filter(query).order_by('id')

            for salary in salary_all:
                info = {
                    'teacher_name': salary.teacher.user.name,
                    'reason': salary.reason,
                    'salary': salary.salary,
                    'account_type': salary.account_type.name,
                    'date': f'{salary.day.year_id} - {salary.day.month_id} - {salary.day.id}'
                }
                filtered_salary.append(info)

        else:
            query = Q(deleted_worker_salary_inDay__isnull=True)
            if year:
                query &= Q(day__year_id=year)
            if month:
                query &= Q(day__month_id=month)
            if day:
                query &= Q(day__id=day)

            salary_all = WorkerSalaryInDay.objects.filter(query).order_by('id')

            for salary in salary_all:
                info = {
                    'worker_name': salary.worker_salary.worker.user.name,
                    'worker_job': salary.worker_salary.worker.job.name,
                    'reason': salary.reason,
                    'salary': salary.salary,
                    'account_type': salary.account_type.name,
                    'date': f'{salary.day.year_id} - {salary.day.month_id} - {salary.day.id}'
                }
                filtered_salary.append(info)

        return Response({
            'filtered_salary': filtered_salary
        })
