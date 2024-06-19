from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('about_us_jobs/', include('Calendar.urls')),
    path('account/', include('account.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('base_route/', include('base_rout.urls')),

    path('Calendar/', include('Calendar.urls')),
    path('Class/', include('Class.urls')),
    path('Contract/', include('contract.urls')),
    path('Flows/', include('Flow.urls')),
    path('Galery/', include('Galery.urls')),
    path('Job/', include('Jobs.urls')),
    path('Partners/', include('Partners.urls')),
    path('Rooms/', include('Rooms.urls')),
    path('Student/', include('Students.urls')),
    path('Subjects/', include('Subjects.urls')),
    path('Teachers/', include('Teachers.urls')),
    path('timetable/', include('timetable.urls')),
    path('lesson_plan/', include('Lesson_plan.urls')),

    path('Vacations/', include('Vacations.urls')),
    path('Worker/', include('Workers.urls')),
]

urlpatterns += doc_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
