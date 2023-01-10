from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    #testser
    path('test/create_test/',create_test, name = 'create_test'),
    path('test/create_test/<int:testid>/create_questions/',create_questions, name = "create_questions"),
    path('test/geturl/<int:testid>', geturl, name = "geturl"),
    path('test/start_a_test/<int:testid>', start_a_test, name = "start_a_test"),
    path('test/start_a_test/<int:testid>/take_test/<int:current_question_num>/<int:taken_test_id>/', take_test, name = "take_test"),
    # path('test/storage/test_list', TestList.as_view(), name = "test_list"),
    path('test/show_result/<int:taken_test_id>', show_result, name = "show_result"),
    path('test/show_result_table/<int:taken_test_id>', show_result_table, name = "show_result_table"),

    #login
    path('login/', login_form, name = "login_form"),
    # path('register/', General.register, name = "register"),
    path('log_out/', log_out, name = "log_out"),


    #main
    path('',homepage, name = "homepage"),




    #student_views:
    path('student/tasks/',s_tasks, name = "s_tasks"),
    path('student/subjects/',s_subjects, name = "s_subjects"),
    path('student/statistics/',s_statistics, name = "s_statistics"),
    path('student/profile/',s_profile, name = "s_profile"),



    #Teacher_views:
    path('teacher/task/<str:task_type>/<int:task_id>',t_task, name = "t_task"),
    path('teacher/create_task/<int:subject_id>/<str:task_type>',t_create_task, name = "t_create_task"),
    path('teacher/choose_task_type/<int:subject_id>',t_choose_task_type, name = "t_choose_task_type"),
    path('teacher/subjects/',t_subjects, name = "t_subjects"),
    path('teacher/statistics/',t_statistics, name = "t_statistics"),
    path('teacher/profile/',t_profile, name = "t_profile"),
    path('teacher/subject/<int:subj_id>',t_subject, name = "t_subject"),
    path('teacher/student_answers',t_student_answers, name = "t_student_answers"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
