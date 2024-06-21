from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterStudent.as_view(), name='register_student'),
    path('student/', StudentList.as_view(), name='student_list'),
    path('student/<int:pk>/', StudentProfile.as_view(), name='student_profile'),
    path('not_in_class_student/', NotInClassStudentView.as_view(), name='not_in_class_student'),
    path('join_class/', JoinClassView.as_view(), name='join_class'),
    path('edit_user_password/', EditUserPasswordView.as_view(), name='edit_user_password'),
    path('edit_username/', EditUsernameView.as_view(), name='edit_username'),
    path('old_student/', OldStudentView.as_view(), name='old_student'),
    path('pdf_contract/<int:student_id>/', PdfContractView.as_view(), name='pdf_contract'),
    path('search_not_student_in_class/', SearchNotInClassStudentView.as_view(), name='search_not_student_in_class'),
    path('search_student_in_class/', SearchInClassStudentView.as_view(), name='search_student_in_class'),
    path('delete_student/', DeleteStudentView.as_view(), name='delete_student'),
    path('deleted_students/', DeletedStudentsView.as_view(), name='deleted_students'),
    path('return_students/', ReturnStudentsView.as_view(), name='return_students'),
    path('filter_delete_student/', FilterDeleteStudentView.as_view(), name='filter_delete_student'),
    path('search_delete_student/', SearchDeleteStudentView.as_view(), name='search_delete_student'),

]
