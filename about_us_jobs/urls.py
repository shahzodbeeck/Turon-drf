from django.urls import path
from .views import AboutFrontView, GetAboutProfileView, InfosView, EditInfoView, DeleteInfoView

urlpatterns = [
    path('about_front/<int:type_id>/<int:info_id>/', AboutFrontView.as_view(), name='about_front'),
    path('get_about_profile/<int:type_id>/<int:info_id>/', GetAboutProfileView.as_view(), name='get_about_profile'),
    path('infos/<int:type_id>/', InfosView.as_view(), name='infos'),
    path('edit_info/<int:info_id>/', EditInfoView.as_view(), name='edit_info'),
    path('delete_info/<int:info_id>/', DeleteInfoView.as_view(), name='delete_info'),
]
