from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Subjects/', include('Subjects.urls')),
    path("Teachers/", include('Teachers.urls')),
    path("Rooms/", include('Rooms.urls')),
    path("Class/", include('Class.urls')),
    path("Student/", include('Students.urls')),
    path("Flows/", include('Flow.urls')),
    path("Galery/", include('Galery.urls')),
    path("Partners/", include('Partners.urls')),
    path("Vacations/", include('Vacations.urls')),
    path("Contract/", include('contract.urls')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
urlpatterns += doc_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
