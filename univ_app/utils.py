from .models import CommonTask, Test, InfoTask
from django.shortcuts import get_object_or_404
#
def get_task(task_type, task_id):
    if task_type == "CommonTask":
        return get_object_or_404(CommonTask, id = task_id)
    if task_type == "Test":
        return get_object_or_404(Test, id = task_id)
    if task_type == "InfoTask":
        return get_object_or_404(InfoTask, id = task_id)
