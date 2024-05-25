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


def _get_student_average_grade(
    student,
    evaluated_answered_common_tasks,
    taken_test_grades,
    answered_common_tasks,
    taken_tests,
) -> int:
    student_answered_common_tasks_grades = evaluated_answered_common_tasks.filter(student=student).values_list(
        "grade", flat=True
    )
    student_taken_tests_grades = taken_test_grades.filter(student=student).values_list(
        "grade", flat=True
    )
    student_all_passed_tasks_cnt = (
            answered_common_tasks.filter(student=student).exclude(status="PASSED").count()
            + taken_tests.filter(student=student).exclude(status="PASSED").count()
    )
    if student_all_passed_tasks_cnt:
        avg_student_grade = (sum(student_answered_common_tasks_grades) + sum(
            student_taken_tests_grades)) / student_all_passed_tasks_cnt
        return avg_student_grade
    return 0


def _is_last_question(questions, current_question_num:int):
    return current_question_num > len(questions)


def _save_previous_question(
        questions,
        current_question_num,
        taken_test,
        request_post
):
    previous_question = questions[current_question_num - 1]
    previous_answered_question = AnsweredQuestion()
    previous_answered_question.related_taken_test = taken_test
    previous_answered_question.related_question = previous_question

    previous_answers = Answer.get_answers(previous_question)
    for i in range(len(previous_answers)):
        checked = request_post.get(f"givenanswer_set-{i}-checked", "off")
        given_answer = GivenAnswer()
        given_answer.checked = checked == "on"
        given_answer.related_answered_question = previous_answered_question
        given_answer.save()

    all_previous_given_answers = GivenAnswer.objects.filter(
        related_answered_question=previous_answered_question
    )
    previous_answered_question.correct = all(
        ans.is_right == prev_ans.checked
        for ans, prev_ans in zip(previous_answers, all_previous_given_answers)
    )
    previous_answered_question.save()