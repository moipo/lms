from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),

    # tests
    path("test/create_test/<int:subject_id>", create_test, name="create_test"),
    path(
        "test/create_test/<int:testid>/create_questions/",
        create_questions,
        name="create_questions",
    ),
    path(
        "test/finish_test_creation/<int:testid>",
        finish_test_creation,
        name="finish_test_creation",
    ),
    path("test/start_a_test/<int:testid>", start_a_test, name="start_a_test"),
    path(
        "test/start_a_test/<int:testid>/take_test/<int:next_question_num>/<int:taken_test_id>/",
        take_test,
        name="take_test",
    ),
    path("test/show_result/<int:taken_test_id>", show_result, name="show_result"),
    path(
        "test/show_result_table/<int:taken_test_id>",
        show_result_table,
        name="show_result_table",
    ),

    # authorization
    path("login/", login_form, name="login_form"),
    path("log_out/", log_out, name="log_out"),

    # Student_views:
    path("student/tasks/", s_tasks, name="s_tasks"),
    path("student/statistics/", s_statistics, name="s_statistics"),
    path(
        "student/answer_task/<str:task_type>/<int:task_id>",
        s_answer_task,
        name="s_answer_task",
    ),
    path("student/group_files/", s_group_files, name="s_group_files"),
    path(
        "student/group_files/subject/<int:subject_id>",
        s_group_files_subject,
        name="s_group_files_subject",
    ),
    path(
        "student/delete_doc/<int:subject_id>/<int:doc_id>/",
        delete_doc,
        name="delete_doc",
    ),
    # Teacher_views:
    path("teacher/task_answers", t_task_answers, name="t_task_answers"),
    path("teacher/task_answer/<int:ans_task_id>", t_task_answer, name="t_task_answer"),
    path(
        "teacher/create_task/<int:subject_id>/<str:task_type>",
        t_create_task,
        name="t_create_task",
    ),
    path(
        "teacher/choose_task_type/<int:subject_id>",
        t_choose_task_type,
        name="t_choose_task_type",
    ),
    path("teacher/statistics/", t_statistics, name="t_statistics"),
    path(
        "teacher/statistics_subject/<int:subject_id>",
        t_statistics_subject,
        name="t_statistics_subject",
    ),
    # Mutual_views
    path("", login_form, name="login_form"),
    path("profile/", ts_profile, name="ts_profile"),
    path("subjects/", ts_subjects, name="ts_subjects"),
    path("subject/<int:subj_id>", ts_subject, name="ts_subject"),
    path("task/<str:task_type>/<int:task_id>", ts_task, name="ts_task"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
