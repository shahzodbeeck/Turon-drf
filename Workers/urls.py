from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WorkerViewSet, WorkerSalaryViewSet, WorkerSalaryInDayViewSet, DeletedWorkerSalaryInDayViewSet, \
    get_worker_salary, worker, worker_profile, worker_salary_detail, worker_salaries_in_month, \
    change_worker_salary_account_type, given_worker_salary, set_worker_salary, delete_worker_given_salary, \
    register_worker, AccountTypeViewSet

router = DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'account_type', AccountTypeViewSet)

router.register(r'worker-salaries', WorkerSalaryViewSet)
router.register(r'worker-salaries-in-day', WorkerSalaryInDayViewSet)
router.register(r'deleted-worker-salaries-in-day', DeletedWorkerSalaryInDayViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-worker-salary/', get_worker_salary),
    path('worker/', worker),
    path('worker-profile/<int:worker_id>/', worker_profile),
    path('worker-salary/<int:worker_id>/', worker_salary_detail),
    path('worker-salaries-in-month/<int:worker_salary_id>/', worker_salaries_in_month),
    path('change-worker-salary-account-type/', change_worker_salary_account_type),
    path('given-worker-salary/', given_worker_salary),
    path('set-worker-salary/', set_worker_salary),
    path('delete-worker-given-salary/', delete_worker_given_salary),
    path('register-worker/', register_worker),
]
