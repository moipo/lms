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
    path('test/create_test/',Tester.create_test, name = 'create_test'),
    path('test/create_test/<int:testid>/create_questions/',Tester.create_questions, name = "create_questions"),
    path('test/geturl/<int:testid>', Tester.geturl, name = "geturl"),
    path('test/start_a_test/<int:testid>', Tester.start_a_test, name = "start_a_test"),
    path('test/start_a_test/<int:testid>/take_test/<int:current_question_num>/<int:taken_test_id>/', Tester.take_test, name = "take_test"),
    # path('test/storage/test_list', TestList.as_view(), name = "test_list"),
    path('test/show_result/<int:taken_test_id>', Tester.show_result, name = "show_result"),
    path('test/show_result_table/<int:taken_test_id>', Tester.show_result_table, name = "show_result_table"),

    #login
    path('login/', Login.login_form, name = "login_form"),
    # path('register/', General.register, name = "register"),
    path('log_out/', Login.log_out, name = "log_out"),


    #main
    path('',Main.homepage, name = "homepage"),




    #student_views:
    path('s_tasks/',Student_views.s_tasks, name = "s_tasks"),
    path('s_subjects/',Student_views.s_subjects, name = "s_subjects"),

    path('s_statistics/',Student_views.s_statistics, name = "s_statistics"),
    path('s_profile/',Student_views.s_profile, name = "s_profile"),



    #Teacher_views:
    path('t_task/<str:task_type>/<int:task_id>',Teacher_views.t_task, name = "t_task"),

    path('t_subjects/',Teacher_views.t_subjects, name = "t_subjects"),
    path('t_statistics/',Teacher_views.t_statistics, name = "t_statistics"),
    path('t_profile/',Teacher_views.t_profile, name = "t_profile"),
    path('t_subject/<int:subj_id>',Teacher_views.t_subject, name = "t_subject"),
    path('t_tasks',Teacher_views.t_tasks, name = "t_tasks"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
