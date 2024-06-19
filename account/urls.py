# urls.py
from django.urls import path
from .views import CollectionView, SearchView, AddPaymentView, PaymentListView, PaymentInMonthView, AddCostView, \
    AllPaymentsView, AddDiscountView, CheckDiscountView, DeletePaymentView, DeleteCostView, DeleteSalaryWorkerView, \
    DeleteSalaryTeacherView, SearchPayView, SearchCostView, FilterSalaryView, FilterDateView

urlpatterns = [
    path('collection/', CollectionView.as_view(), name='collection'),
    path('search/', SearchView.as_view(), name='search'),
    path('add_payment/<int:student_id>/', AddPaymentView.as_view(), name='add_payment'),
    path('payment_list/<int:student_id>/', PaymentListView.as_view(), name='payment_list'),
    path('payment_in_month/<int:month_payment_id>/', PaymentInMonthView.as_view(), name='payment_in_month'),
    path('add_cost/', AddCostView.as_view(), name='add_cost'),
    path('all_payments/<str:type_request>/<int:page_num>/', AllPaymentsView.as_view(), name='all_payments'),
    path('add_discount/<int:student_id>/', AddDiscountView.as_view(), name='add_discount'),
    path('check_discount/', CheckDiscountView.as_view(), name='check_discount'),
    path('delete_payment/', DeletePaymentView.as_view(), name='delete_payment'),
    path('delete_cost/', DeleteCostView.as_view(), name='delete_cost'),
    path('delete_salary_worker/', DeleteSalaryWorkerView.as_view(), name='delete_salary_worker'),
    path('delete_salary_teacher/', DeleteSalaryTeacherView.as_view(), name='delete_salary_teacher'),
    path('search_pay/', SearchPayView.as_view(), name='search_pay'),
    path('search_cost/', SearchCostView.as_view(), name='search_cost'),
    path('filter_salary/', FilterSalaryView.as_view(), name='filter_salary'),
    path('filter_date/', FilterDateView.as_view(), name='filter_date'),

]
