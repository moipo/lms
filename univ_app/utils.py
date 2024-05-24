from .models import *
from django.shortcuts import get_object_or_404


def get_task(task_type, task_id):
    if task_type == "CommonTask":
        return get_object_or_404(CommonTask, id=task_id)
    if task_type == "Test":
        return get_object_or_404(Test, id=task_id)
    if task_type == "InfoTask":
        return get_object_or_404(InfoTask, id=task_id)


def is_teacher(user) -> bool:
    if user.groups.filter(name="teacher").exists():
        return True
    else:
        return False


def create_answered_task_instances_for_group(task):
    student_set = task.subject.st_group.student_set.all()
    task_type = task.get_type()
    if task_type == "CommonTask":
        for student in student_set:
            AnsweredCommonTask.objects.create(
                student=student, common_task=task, status=AnsweredTask.ASND
            )
    elif task_type == "Test":
        for student in student_set:
            TakenTest.objects.create(
                student=student, related_test=task, status=AnsweredTask.ASND
            )
    elif task_type == "InfoTask":
        for student in student_set:
            AnsweredInfoTask.objects.create(
                student=student, related_info_task=task, status=AnsweredTask.ASND
            )


def get_ans_task(task, student):
    task_type = task.get_type()
    if task_type == "CommonTask":
        ans_task = AnsweredCommonTask.objects.get(common_task=task, student=student)
    elif task_type == "Test":
        ans_task = TakenTest.objects.get(related_test=task, student=student)
    elif task_type == "InfoTask":
        ans_task = AnsweredInfoTask.objects.get(related_info_task=task, student=student)
    return ans_task
