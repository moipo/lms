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

    path('test/create_test/',General.create_test, name = 'create_test'),
    path('test/create_test/<int:testid>/create_questions/',General.create_questions, name = "create_questions"),
    path('test/geturl/<int:testid>', General.geturl, name = "geturl"),
    path('test/start_a_test/<int:testid>', General.start_a_test, name = "start_a_test"),
    path('test/start_a_test/<int:testid>/take_test/<int:current_question_num>/<int:taken_test_id>/', General.take_test, name = "take_test"),
    # path('test/storage/test_list', TestList.as_view(), name = "test_list"),
    path('test/show_result/<int:taken_test_id>', General.show_result, name = "show_result"),
    path('test/show_result_table/<int:taken_test_id>', General.show_result_table, name = "show_result_table"),

    #login
    path('login/', General.login_form, name = "login_form"),
    # path('register/', General.register, name = "register"),
    path('log_out/', General.log_out, name = "log_out"),


    #main
    path('',Main.homepage, name = "homepage"),
    path('profile/',Main.profile, name = "profile"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
