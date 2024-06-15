
from django.urls import path
from .views import CreateContractView, DownloadView

urlpatterns = [
    path('create_contract/<int:student_id>/', CreateContractView.as_view(), name='create-contract'),
    path('download/<path:filename>/', DownloadView.as_view(), name='download-file'),
]
