from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TimeTableDayViewSet,
    TimeListViewSet,
    DailyTableViewSet,
    CheckTimetableAPIView,
    CreateTimetableAPIView,
    TimetablesAPIView,
    CreateTableAPIView,
    DeleteItemInLessonAPIView,
    FlowTimetableAPIView,
    CreateFlowTimetableAPIView,
    DeleteFlowItemInLessonAPIView,
    LessonTableAPIView
)

router = DefaultRouter()
router.register(r'timetable_days', TimeTableDayViewSet)
router.register(r'time_lists', TimeListViewSet)
router.register(r'daily_tables', DailyTableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check-timetable/', CheckTimetableAPIView.as_view(), name='check_timetable'),

    path('creat_timetable/<int:class_id>/', CreateTimetableAPIView.as_view(), name='create_timetable'),
    path('timetables/', TimetablesAPIView.as_view(), name='timetables'),
    path('creat_table/', CreateTableAPIView.as_view(), name='create_table'),
    path('delete_item_in_lesson/', DeleteItemInLessonAPIView.as_view(), name='delete_item_in_lesson'),
    path('flow_timetable/', FlowTimetableAPIView.as_view(), name='flow_timetable'),
    path('creat_flow_timetable/', CreateFlowTimetableAPIView.as_view(), name='create_flow_timetable'),
    path('delete_flow_item_in_lesson/', DeleteFlowItemInLessonAPIView.as_view(), name='delete_flow_item_in_lesson'),
    path('lesson_table/', LessonTableAPIView.as_view(), name='lesson_table'),
]
