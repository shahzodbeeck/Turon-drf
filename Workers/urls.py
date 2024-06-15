from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    WorkerViewSet, WorkerSalaryViewSet, WorkerSalaryInDayViewSet, DeletedWorkerSalaryInDayViewSet,
    GetWorkerSalaryView, WorkerListView, WorkerProfileView, WorkerSalaryDetailView,
    WorkerSalariesInMonthView, ChangeWorkerSalaryAccountTypeView, GivenWorkerSalaryView,
    SetWorkerSalaryView, DeleteWorkerGivenSalaryView, RegisterWorkerView, AccountTypeViewSet
)

router = DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'account_type', AccountTypeViewSet)
router.register(r'worker-salaries', WorkerSalaryViewSet)
router.register(r'worker-salaries-in-day', WorkerSalaryInDayViewSet)
router.register(r'deleted-worker-salaries-in-day', DeletedWorkerSalaryInDayViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-worker-salary/', GetWorkerSalaryView.as_view(), name='get-worker-salary'),
    path('worker/', WorkerListView.as_view(), name='worker-list'),
    path('worker-profile/<int:worker_id>/', WorkerProfileView.as_view(), name='worker-profile'),
    path('worker-salary/<int:worker_id>/', WorkerSalaryDetailView.as_view(), name='worker-salary-detail'),
    path('worker-salaries-in-month/<int:worker_salary_id>/', WorkerSalariesInMonthView.as_view(), name='worker-salaries-in-month'),
    path('change-worker-salary-account-type/', ChangeWorkerSalaryAccountTypeView.as_view(), name='change-worker-salary-account-type'),
    path('given-worker-salary/', GivenWorkerSalaryView.as_view(), name='given-worker-salary'),
    path('set-worker-salary/', SetWorkerSalaryView.as_view(), name='set-worker-salary'),
    path('delete-worker-given-salary/', DeleteWorkerGivenSalaryView.as_view(), name='delete-worker-given-salary'),
    path('register-worker/', RegisterWorkerView.as_view(), name='register-worker'),
]
