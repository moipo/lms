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
    ans_common_tasks = AnsweredCommonTask.objects.filter(student = student, status = AnsweredTask.ASND)
    taken_tests = TakenTest.objects.filter(student = student, status = AnsweredTask.ASND)
    info_tasks = AnsweredInfoTask.objects.filter(student = student, status = AnsweredTask.ASND)
    not_done_tasks = list(chain(ans_common_tasks, taken_tests, info_tasks))
    # ans_tasks.sort(key = lambda task : task.finished_at)
    return not_done_tasks


def get_all_done_tasks(student):
    ans_common_tasks = AnsweredCommonTask.objects.filter(student = student, status = AnsweredTask.DONE)
    taken_tests = TakenTest.objects.filter(student = student, status = AnsweredTask.DONE)
    info_tasks = AnsweredInfoTask.objects.filter(student = student, status = AnsweredTask.DONE)
    done_tasks = list(chain(ans_common_tasks, taken_tests, info_tasks))
    # ans_tasks.sort(key = lambda task : task.finished_at)
    return done_tasks


def create_answered_task_instances_for_group(task):
    student_set = task.subject.st_group.student_set.all()
    task_type = task.get_type()
    if task_type == "CommonTask": 
        for student in student_set:
            AnsweredCommonTask.objects.create(student = student, common_task = task, status = AnsweredTask.ASND)
    elif task_type == "Test":
        for student in student_set:
            TakenTest.objects.create(student = student, related_test = task, status = AnsweredTask.ASND)
    elif task_type == "InfoTask":
        for student in student_set:
            AnsweredInfoTask.objects.create(student = student, related_info_task = task, status = AnsweredTask.ASND)