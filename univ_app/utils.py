from .models import *
from django.shortcuts import get_object_or_404

def get_task(task_type, task_id):
    if task_type == "CommonTask":
        return get_object_or_404(CommonTask, id = task_id)
    if task_type == "Test":
        return get_object_or_404(Test, id = task_id)
    if task_type == "InfoTask":
        return get_object_or_404(InfoTask, id = task_id)

def is_teacher(user):
    if user.groups.filter(name = "teacher").exists(): return True
    else: return False


def get_all_not_done_tasks(student):
    ans_common_tasks = AnsweredCommonTask.objects.filter(student = student, was_done = False)
    taken_tests = TakenTest.objects.filter(student = student, was_done = False)
    info_tasks = AnsweredInfoTask.objects.filter(student = student, was_done = False)
    not_done_tasks = list(chain(ans_common_tasks, taken_tests, info_tasks))
    # ans_tasks.sort(key = lambda task : task.finished_at)
    return not_done_tasks


def get_all_done_tasks(student):
    ans_common_tasks = AnsweredCommonTask.objects.filter(student = student, was_done = True)
    taken_tests = TakenTest.objects.filter(student = student, was_done = True)
    info_tasks = AnsweredInfoTask.objects.filter(student = student, was_done = True)
    done_tasks = list(chain(ans_common_tasks, taken_tests, info_tasks))
    # ans_tasks.sort(key = lambda task : task.finished_at)
    return done_tasks