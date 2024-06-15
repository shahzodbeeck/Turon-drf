import calendar
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from turon.permission import IsAdminOrReadOnly
from .models import Years, Month, Day, TypeDay
from .serializers import YearsSerializer, MonthSerializer, DaySerializer, TypeDaySerializer


class YearsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Years.objects.all()
    serializer_class = YearsSerializer


class MonthViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Month.objects.all()
    serializer_class = MonthSerializer


class DayViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class TypeDayViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = TypeDay.objects.all()
    serializer_class = TypeDaySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def get_calendar(request, current_year, next_year):
    list_days = []
    for year in range(current_year, next_year + 1):
        for month in range(1, 13):
            if (year == current_year and month not in [1, 2, 3, 4, 5, 6, 7, 8]) or (
                    year == next_year and month not in [9, 10, 11, 12]):
                month_name = calendar.month_name[month]
                object_days = {
                    'month_number': month,
                    'month_name': month_name,
                    'days': [],
                    'year': year
                }
                cal = calendar.monthcalendar(year, month)
                for week in cal:
                    for day in week:
                        day_str = str(day) if day != 0 else "  "
                        if day != 0:
                            if 1 <= day <= calendar.monthrange(year, month)[1]:
                                weeks_id = calendar.weekday(year, month, day)
                                day_name = calendar.day_name[weeks_id]
                            day_object = {
                                'day_number': day_str,
                                'day_name': day_name
                            }
                            object_days['days'].append(day_object)
                list_days.append(object_days)

    for year_data in list_days:
        year_obj, created = Years.objects.get_or_create(year=year_data['year'])
        for month_data in list_days:
            if month_data['year'] == year_data['year']:
                month_obj, created = Month.objects.get_or_create(
                    month_number=month_data['month_number'],
                    years=year_obj,
                    defaults={'month_name': month_data['month_name']}
                )
                for day_data in month_data['days']:
                    type_day_instance = TypeDay.objects.get(id=1 if day_data['day_name'] == 'Sunday' else 2)
                    Day.objects.get_or_create(
                        day_number=day_data['day_number'],
                        month=month_obj,
                        year=year_obj,
                        defaults={'day_name': day_data['day_name'], 'type_id': type_day_instance}
                    )

    return Response(list_days,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def change_type(request):
    day_id = request.data.get('day_id')
    type_id = request.data.get('type_id')
    Day.objects.filter(id=day_id).update(type_id=type_id)
    color = TypeDay.objects.get(id=type_id).color
    return Response({'color': color}, status=status.HTTP_200_OK)
