from django.urls import path
from .views import FlowView, FilterStudentForFlowView, CreateFlowView, JoinFlowView, FlowProfileView, TransferStudentsInFlowView, DeleteStudentInFlowView, DeleteFlowView

urlpatterns = [
    path('flow/', FlowView.as_view(), name='flow'),
    path('filter_student_for_flow/', FilterStudentForFlowView.as_view(), name='filter_student_for_flow'),
    path('create_flow/', CreateFlowView.as_view(), name='create_flow'),
    path('join_flow/', JoinFlowView.as_view(), name='join_flow'),
    path('flow_profile/<int:flow_id>/', FlowProfileView.as_view(), name='flow_profile'),
    path('transfer_students_in_flow/', TransferStudentsInFlowView.as_view(), name='transfer_students_in_flow'),
    path('delete_student_in_flow/', DeleteStudentInFlowView.as_view(), name='delete_student_in_flow'),
    path('delete_flow/', DeleteFlowView.as_view(), name='delete_flow'),
]
