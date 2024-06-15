from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YearsViewSet, MonthViewSet, DayViewSet, TypeDayViewSet, CalendarView, ChangeTypeView

router = DefaultRouter()
router.register(r'years', YearsViewSet)
router.register(r'months', MonthViewSet)
router.register(r'days', DayViewSet)
router.register(r'type_days', TypeDayViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-calendar/<int:current_year>/<int:next_year>/', CalendarView.as_view(), name='get-calendar'),
    path('change-type/', ChangeTypeView.as_view(), name='change-type'),
]
