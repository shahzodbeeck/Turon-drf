from django.urls import path
from .views import (
    ClassesView, FilterClassesView, CreateClassView, ClassProfileView,
    EditClassView, DeleteStudentInClassView, TransferStudentsInClassView,
    DeleteClassView, ClassSubjectsView, AddClassSubjectsView
)

urlpatterns = [
    path('classes/', ClassesView.as_view(), name='classes'),
    path('filter_classes/', FilterClassesView.as_view(), name='filter_classes'),
    path('create_class/', CreateClassView.as_view(), name='create_class'),
    path('class_profile/<int:class_id>/', ClassProfileView.as_view(), name='class_profile'),
    path('edit_class/<int:class_id>/', EditClassView.as_view(), name='edit_class'),
    path('delete_student_in_class/', DeleteStudentInClassView.as_view(), name='delete_student_in_class'),
    path('transfer_students_in_class/', TransferStudentsInClassView.as_view(), name='transfer_students_in_class'),
    path('delete_class/', DeleteClassView.as_view(), name='delete_class'),
    path('class_subjects/<int:class_id>/', ClassSubjectsView.as_view(), name='class_subjects'),
    path('add_class_subjects/', AddClassSubjectsView.as_view(), name='add_class_subjects'),
]
