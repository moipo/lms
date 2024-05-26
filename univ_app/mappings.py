from collections.abc import Mapping

from django.forms import ModelForm

from univ_app.enums import TaskTypes
from univ_app.forms import CommonTaskForm, InfoTaskForm
from univ_app.models import AnsweredTask

task_form_by_task_type_mapping: Mapping[TaskTypes:ModelForm] = {
    TaskTypes.common_task.value: CommonTaskForm,
    TaskTypes.info_task.value: InfoTaskForm,
}

status_by_condition_mapping: Mapping[(bool, bool)] = {
    # condition: (task_was_accepted, grade_is_present)
    (False, False): AnsweredTask.ASSIGNED,
    (False, True): AnsweredTask.ASSIGNED,
    (True, False): AnsweredTask.PASSED,
    (True, True): AnsweredTask.EVALUATED,
}
