from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404

from .enums import TaskTypes
from .models import *


def get_task(task_type, task_id):
    if task_type == TaskTypes.common_task.value:
        return get_object_or_404(CommonTask, id=task_id)
    if task_type == TaskTypes.test.value:
        return get_object_or_404(Test, id=task_id)
    if task_type == TaskTypes.info_task.value:
        return get_object_or_404(InfoTask, id=task_id)


def is_teacher(user) -> bool:
    return user.groups.filter(name="teacher").exists()


def create_answered_task_instances_for_group(task):
    student_set = task.subject.st_group.student_set.all()
    task_type = task.get_type()
    if task_type == "CommonTask":
        for student in student_set:
            AnsweredCommonTask.objects.create(
                student=student, common_task=task, status=AnsweredTask.ASSIGNED
            )
    elif task_type == "Test":
        for student in student_set:
            TakenTest.objects.create(
                student=student, related_test=task, status=AnsweredTask.ASSIGNED
            )
    elif task_type == "InfoTask":
        for student in student_set:
            AnsweredInfoTask.objects.create(
                student=student, related_info_task=task, status=AnsweredTask.ASSIGNED
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


def _get_student_average_grade(
    student,
    evaluated_answered_common_tasks,
    taken_test_grades,
    answered_common_tasks,
    taken_tests,
) -> int:
    student_answered_common_tasks_grades = evaluated_answered_common_tasks.filter(
        student=student
    ).values_list("grade", flat=True)
    student_taken_tests_grades = taken_test_grades.filter(student=student).values_list(
        "grade", flat=True
    )
    student_all_passed_tasks_cnt = (
        answered_common_tasks.filter(student=student).exclude(status="PASSED").count()
        + taken_tests.filter(student=student).exclude(status="PASSED").count()
    )
    if student_all_passed_tasks_cnt:
        avg_student_grade = (
            sum(student_answered_common_tasks_grades) + sum(student_taken_tests_grades)
        ) / student_all_passed_tasks_cnt
        return round(avg_student_grade, 2)
    return 0


def _is_last_question(questions, next_question_num: int) -> bool:
    print(f"next_qestion_num: {next_question_num} \n len(questions) {len(questions)}")
    return next_question_num == len(questions)


def _save_previous_question(
    questions, next_question_num, taken_test, request_post
) -> None:
    previous_question = questions[next_question_num - 1]
    previous_answered_question = AnsweredQuestion.objects.create(
        related_taken_test=taken_test,
        related_question=previous_question,
    )

    previous_answers = Answer.get_answers(previous_question)
    for i in range(len(previous_answers)):
        checked = request_post.get(f"givenanswer_set-{i}-checked", "off")
        given_answer = GivenAnswer.objects.create(
            checked=checked == "on",
            related_answered_question=previous_answered_question,
        )

    all_previous_given_answers = GivenAnswer.objects.filter(
        related_answered_question=previous_answered_question
    )
    previous_answered_question.correct = all(
        ans.is_right == prev_ans.checked
        for ans, prev_ans in zip(previous_answers, all_previous_given_answers)
    )
    previous_answered_question.save()


def _get_zipped_answers_and_given_answers_forms(
    answers,
    request_method,
):
    GivenAnswerFormSet = inlineformset_factory(
        AnsweredQuestion,
        GivenAnswer,
        fields=("checked",),
        labels={"checked": ""},
        can_delete_extra=False,
        extra=2 if request_method == "POST" else len(answers),
    )
    givenanswer_formset = GivenAnswerFormSet()
    return zip(answers, givenanswer_formset)
