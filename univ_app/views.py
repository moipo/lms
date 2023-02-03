from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.urls import reverse
from django.forms import inlineformset_factory
from .decorators import allowed_users
from .utils import get_task, is_teacher, create_answered_task_instances_for_group, get_ans_task
from collections import Counter
from django.contrib import messages
import datetime
import pytz


def homepage(request):
    return render(request,"homepage/homepage.html",{})



@allowed_users(allowed_groups = ["teacher"])
def t_choose_task_type(request, subject_id):
    return render(request,"teacher_views/t_choose_task_type.html",{"subject_id":subject_id})


@allowed_users(allowed_groups = ["teacher"])
def t_create_task(request, subject_id = None, task_type=None):
    
    teacher = request.user.teacher

    if request.method == "POST":
        if task_type == "CommonTask": form = CommonTaskForm(request.POST, request.FILES)
        elif task_type == "InfoTask": form = InfoTaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = teacher
            task.subject = Subject.objects.get(id = subject_id)
            task.save()
            create_answered_task_instances_for_group(task)
            messages.success(request, "Задание было успешно создано и опубликовано")
            return redirect('ts_subject', subject_id)

    if task_type == "CommonTask": form = CommonTaskForm()
    elif task_type == "InfoTask": form = InfoTaskForm()
    elif task_type == "Test": return redirect("create_test", subject_id = subject_id)
    
    ctx = {
    "task_type":task_type,
    "form":form,
    "subject_id":subject_id,
    }
    
    return render(request,"teacher_views/t_create_common_task.html",ctx)


@allowed_users(allowed_groups = ["teacher"])
def t_statistics(request):
    teacher = request.user.teacher
    subjects = Subject.objects.all().filter(teacher = teacher)
    ctx = {
    "subjects":subjects,
    }
    return render(request,"teacher_views/t_statistics.html",ctx)


@allowed_users(allowed_groups = ["teacher"])
def t_statistics_subject(request, subject_id):
    
    subject = Subject.objects.get(id = subject_id)
    
    common_tasks = subject.commontask_set.all()
    tests = subject.test_set.all()
    
    ans_common_tasks = AnsweredCommonTask.objects.filter(common_task__in = common_tasks)
    taken_tests = TakenTest.objects.filter(related_test__in = tests)
    
    tasks_amount = taken_tests.count() + ans_common_tasks.count()
    
    
    
    
    #infotask is not considered a task
    
    assigned_tasks_cnt = taken_tests.filter(status = AnsweredTask.ASND).count() + ans_common_tasks.filter(status = AnsweredTask.ASND).count()
    done_tasks_cnt = taken_tests.filter(status = AnsweredTask.DONE).count() + ans_common_tasks.filter(status = AnsweredTask.DONE).count()
    passed_tasks_cnt =  taken_tests.filter(status = AnsweredTask.PSSD).count() + ans_common_tasks.filter(status = AnsweredTask.PSSD).count()
    eval_tasks_cnt = taken_tests.filter(status = AnsweredTask.EVAL).count() + ans_common_tasks.filter(status = AnsweredTask.EVAL).count()
    
    eval_ans_common_tasks  = taken_tests.filter(status = AnsweredTask.EVAL) 
    eval_taken_tests = ans_common_tasks.filter(status = AnsweredTask.EVAL)
    
    ans_common_tasks_grades = eval_ans_common_tasks.values_list("grade", flat = True)
    taken_test_grades = eval_taken_tests.values_list("grade", flat = True)
    
    avg_grade = (sum(ans_common_tasks_grades) + sum(taken_test_grades))/eval_tasks_cnt
    
    students = subject.st_group.student_set.all()
    student_avg_grades = []

    for student in students:
        s_ct_gr = eval_ans_common_tasks.filter(student = student).values_list("grade", flat = True)
        s_tt_gr = taken_test_grades.filter(student = student).values_list("grade", flat = True)
        #avg grade, considering, that if task wasn't done then grade is zero.
        # student_avg_grades.append((sum(s_ct_gr) + sum(s_tt_gr) )/assigned_tasks_cnt+eval_tasks_cnt)
        student_all_tasks_cnt = ans_common_tasks.filter(student = student).exclude(status="PASSED").count() + taken_tests.filter(student=student).exclude(status="PASSED").count()
        avg_grade = (sum(s_ct_gr) + sum(s_tt_gr) )/student_all_tasks_cnt
        # AnsweredCommonTask.objects.filter(student = student).count*
        student_avg_grades.append(round(avg_grade,2) if avg_grade else 0)
                                #   (len(s_ct_gr) + len(s_tt_gr)))
                                #   ) - normal avg

    ctx = {
    "subject":subject,
    "tasks_amount": tasks_amount, 
    "assigned_tasks_cnt":assigned_tasks_cnt,
    "done_tasks_cnt" : done_tasks_cnt,
    "passed_tasks_cnt" : passed_tasks_cnt,
    "eval_tasks_cnt" : eval_tasks_cnt,
    "avg_grade" : avg_grade,
    "students" : students,
    "student_names" : [str(st) for st in students],
    "student_avg_grades" : student_avg_grades,
    }
    return render(request,"teacher_views/t_statistics_subject.html",ctx)


@allowed_users(allowed_groups = ["teacher"])
def t_task_answers(request):
    teacher = request.user.teacher
    t_subjects = teacher.subject_set.all()
    t_common_tasks = CommonTask.objects.filter(subject__in = t_subjects)
    task_answers = AnsweredCommonTask.objects.filter(common_task__in = t_common_tasks , status = AnsweredTask.DONE).order_by("finished_at")
    ctx = {
    "task_answers":task_answers,
    }
    return render(request,"teacher_views/t_task_answers.html", ctx)



@allowed_users(allowed_groups = ["teacher"])
def t_task_answer(request, ans_task_id):
    ans_task = get_object_or_404(AnsweredCommonTask, pk = ans_task_id)
    common_task = ans_task.common_task
    
    if request.method == "POST":
        task_was_accepted = request.POST.get('btn_accepted') is not None
        if task_was_accepted:
            grade = request.POST.get("grade")
            if grade == "":
                ans_task.status = AnsweredTask.PSSD
            else:
                ans_task.grade = int(grade)
                ans_task.status = AnsweredTask.EVAL
        else:
            ans_task.status = AnsweredTask.ASND
        comment = request.POST.get("comment_from_teacher")
        if comment: ans_task.comment_from_teacher = comment
        ans_task.save()
        return redirect('t_task_answers')    
            
    ctx = {
        "common_task": common_task,
        "ans_task":ans_task,
    }
    return render(request,"teacher_views/t_task_answer.html", ctx)






#Student views
@allowed_users(allowed_groups = ["student"])
def s_tasks(request):
    student = request.user.student
    assigned_tasks = student.get_all_tasks_by_type(AnsweredTask.ASND)
    done_tasks = student.get_all_tasks_by_type(AnsweredTask.DONE)
    eval_tasks = student.get_all_tasks_by_type(AnsweredTask.EVAL)
    passed_tasks = student.get_all_tasks_by_type(AnsweredTask.PSSD)
    checked_tasks = student.get_all_tasks_by_type(AnsweredTask.CHKD)
    print(checked_tasks)
    ctx = {
        "assigned_tasks":assigned_tasks,
        "done_tasks":done_tasks,
        "eval_tasks":eval_tasks,
        "passed_tasks":passed_tasks,
        "checked_tasks" : checked_tasks,
    }

    
    return render(request, "student_views/s_tasks.html", ctx)

@allowed_users(allowed_groups = ["student"])
def s_group_files(request):
    st_group = request.user.student.st_group
    subjects = Subject.objects.all().filter(st_group = st_group)
    
    ctx = {
    "subjects":subjects,
    }
    
    return render(request, "student_views/s_group_files.html", ctx)

@allowed_users(allowed_groups = ["student"])
def s_group_files_subject(request,subject_id):
    
    student = request.user.student
    subject = Subject.objects.get(id = subject_id)
    
    
    if request.method == "POST":
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            
            instance = form.save(commit = False)
            instance.student = student
            instance.subject = subject
            instance.save()
        else:
            #implicit iterations clear previous messages
            list(messages.get_messages(request))
            messages.warning(request, "Выбран неверный формат файла")

    
    
    docs = subject.document_set.all()
    form = DocumentForm()
    ctx = {
        "docs":docs,
        "subject" : subject,
        "form":form,
    }
    return render(request, "student_views/s_group_files_subject.html", ctx)




@allowed_users(allowed_groups = ["student"])
def s_statistics(request):
    student = request.user.student
    assigned_tasks = student.get_all_tasks_by_type(AnsweredTask.ASND)
    done_tasks = student.get_all_tasks_by_type(AnsweredTask.DONE)
    eval_tasks = student.get_all_tasks_by_type(AnsweredTask.EVAL)
    passed_tasks = student.get_all_tasks_by_type(AnsweredTask.PSSD)
    
    standart_grades = [task.grade for task in eval_tasks if task.grade in {1,2,3,4,5}]
    grades_cnt = dict.fromkeys([1,2,3,4,5],0)
    for key,value in Counter(standart_grades).items():
        grades_cnt[key] += value
    task_grades = list(grades_cnt.values())
 
    ctx = {
        "assigned_tasks":assigned_tasks,
        "done_tasks":done_tasks,
        "eval_tasks":eval_tasks,
        "passed_tasks":passed_tasks,
        'task_grades' : task_grades,
    } 
    
    
    return render(request, "student_views/s_statistics.html", ctx)


#кнопка "выполнить задание"
@allowed_users(allowed_groups = ["student"])
def s_answer_task(request, task_type = None, task_id = None):
    student = request.user.student
    
    if request.method == "POST":
        if task_type == "CommonTask":
            common_task = CommonTask.objects.get(id = task_id)
            qs = student.answeredcommontask_set.filter(common_task = common_task)
            if qs: last_attempt = qs[0]
            else: last_attempt = None
            form = AnsweredCommonTaskForm(request.POST, request.FILES, instance = last_attempt)
            if form.is_valid():
                answered_common_task = form.save(commit=False)
                answered_common_task.student = student
                answered_common_task.common_task = common_task
                answered_common_task.status = AnsweredTask.DONE
                answered_common_task.finished_at = pytz.UTC.localize(datetime.datetime.now())
                answered_common_task.save()
                messages.success(request,"Ответ на задание был успешно отправлен на проверку.")
                return redirect('s_tasks')
                # return redirect('ts_subject', common_task.subject.id)
            
    if task_type == "CommonTask":
        form = AnsweredCommonTaskForm(request.POST or None)
        ctx = {
        "form":form,
        "task_type":task_type,
        "task_id":task_id,
        }
        return render(request, "student_views/s_answer_task.html", ctx)

    if task_type == "Test":
        return redirect("start_a_test", task_id)

    if task_type == "InfoTask":
        info_task = get_task(task_type, task_id)
        answered_info_task = get_ans_task(info_task,student)
        answered_info_task.status = AnsweredTask.CHKD
        answered_info_task.save()
        return redirect('s_tasks')
        # return redirect('ts_subject', info_task.subject.id)









#Mutual views
@allowed_users(allowed_groups = ["teacher","student"])
def ts_subjects(request):
    user = request.user
    subjects = None
    if is_teacher(user):
        teacher = user.teacher
        subjects = Subject.objects.all().filter(teacher = teacher)
    else:
        student_group = user.student.st_group
        subjects = Subject.objects.all().filter(st_group = student_group)
    ctx = {
    "subjects":subjects,
    }
    return render(request,"mutual_views/ts_subjects.html",ctx)

@allowed_users(allowed_groups = ["teacher", "student"])
def ts_subject(request, subj_id):
    subject = Subject.objects.get(id = subj_id)
    tasks = subject.all_tasks
    ctx = {
    "subject":subject,
    "tasks":tasks,
    }
    return render(request,"mutual_views/ts_subject.html",ctx)

@allowed_users(allowed_groups = ["teacher","student"])
def ts_profile(request):
    ctx = {}
    return render(request,"mutual_views/ts_profile.html",ctx)


@allowed_users(allowed_groups = ["teacher","student"])
def ts_task(request, task_type=0, task_id=0):
    task = get_task(task_type, task_id)
    
    ctx = {
    "task":task
    }
    
    user = request.user
    if not is_teacher(user):
        ans_task = get_ans_task(task, user.student)
        ctx['ans_task'] = ans_task

    return render(request,"mutual_views/ts_task.html",ctx)



































"""
***************************************************************************************************************
                                    Tester (part of an old project):
***************************************************************************************************************
"""










@allowed_users(allowed_groups = ["teacher"])
def create_test(request, subject_id):
    if request.method == "POST":
        form = TestForm(request.POST,request.FILES)
        if form.is_valid():
            test = form.save(commit = False)
            test.subject = Subject.objects.get(id = subject_id)
            test.save()
            return redirect('create_questions', test.pk)

    form = TestForm()
    ctx = {
        "form_test": form,
    }
    return render(request, "tester/create_test/create_test.html", ctx)


@allowed_users(allowed_groups = ["teacher"])
def create_questions(request, testid):
    if request.method == "POST":

        question = request.POST.get('question')

        the_test = Test.objects.get(id = testid)
        previous_questions = Question.get_test_questions(the_test)

        the_question = Question.objects.create(question = question, related_test = the_test)

        answers = request.POST.getlist('answer')
        is_right = request.POST.getlist('is_right')


        for number, answer in enumerate(answers, 1):
             ans_obj = Answer()
             ans_obj.answer = answer
             ans_obj.is_right = str(number) in is_right
             ans_obj.related_question = the_question
             ans_obj.save()

        answer_form_not_model = AnswerFormNotModel()
        ctx = {
        "answer_form_not_model" : answer_form_not_model,
        'testid': testid,
        'previous_questions' : previous_questions,
        }
        return render(request,"tester/create_test/create_questions.html", ctx)
    else:
        answer_form_not_model = AnswerFormNotModel()
        ctx = {
        "answer_form_not_model" : answer_form_not_model,
        'testid': testid,
        }
        return render(request,"tester/create_test/create_questions.html", ctx)

@allowed_users(allowed_groups = ["teacher"])
def finish_test_creation(request, testid):
    test = Test.objects.get(id = testid)
    if Question.objects.filter(related_test=test).count() == 0:
        test.delete()
        ctx = {"subject_id" : test.subject.id }
        return render(request, "tester/create_test/cant_create_test.html",ctx )
    create_answered_task_instances_for_group(test)
    return redirect("ts_subject", test.subject.id)


@allowed_users(allowed_groups = ["student"])
def start_a_test(request, testid):
    the_test = Test.objects.get(id = testid)
    ctx = {
    "the_test":the_test,
    }
    return render(request,"tester/take_test/start_a_test.html", ctx )

@allowed_users(allowed_groups = ["student"])
def take_test(request, testid, current_question_num, taken_test_id):



    if request.method == 'POST':
        the_test = Test.objects.get(pk = testid)
        question_set = Question.get_test_questions(the_test)
        this_question = None


        next_question_num = current_question_num + 1
        if len(question_set) < next_question_num-1:
            next_question = 999999

        taken_test = TakenTest.objects.get(id = taken_test_id)

        ans_length = 2
        try:
            next_question = question_set[current_question_num]
            if next_question is not None:
                next_answers = Answer.objects.filter(related_question = next_question)
                ans_length = len(next_answers)
        except: pass


        GivenAnswerFormSet = inlineformset_factory(
        AnsweredQuestion,
        GivenAnswer,
        fields = ("checked",) ,
        labels = {"checked" : ""},
        can_delete_extra = False,
        extra = ans_length,
        )

        previous_question = question_set[current_question_num-1]

        prev_ans_quest = AnsweredQuestion()
        prev_ans_quest.related_taken_test = taken_test
        prev_ans_quest.related_question = previous_question
        prev_ans_quest.save()


        previous_answers = Answer.get_answers(previous_question)

        for i in range(len(previous_answers)):
            checked = request.POST.get(f"givenanswer_set-{i}-checked","off")
            given_answer = GivenAnswer()
            given_answer.checked = True if checked == "on" else False
            given_answer.related_answered_question = prev_ans_quest
            given_answer.save()






        all_prev_given_ans = GivenAnswer.objects.filter(related_answered_question = prev_ans_quest)

        prev_ans_quest.correct = all([ans.is_right == prev_ans.checked for ans, prev_ans in zip(previous_answers , all_prev_given_ans)])
        prev_ans_quest.save()


        if current_question_num == 999999:
            return redirect(reverse('show_result', args=[taken_test_id]))
        try:
            this_question = question_set[current_question_num]
        except:
            return redirect(reverse('show_result', args=[taken_test_id]))




        the_answers = Answer.get_answers(this_question)
        answered_question = AnsweredQuestion(related_taken_test = taken_test, related_question = this_question)
        givenanswer_formset = GivenAnswerFormSet()
        a_ga_zipped = zip(the_answers, givenanswer_formset)





        ctx = {
            "quantity_of_questions" : len(question_set),
            "this_question": this_question,
            "next_question_num": next_question_num,
            "the_answers" : the_answers,
            "givenanswer_formset" : givenanswer_formset,
            "the_test" : the_test,
            "a_ga_zipped" : a_ga_zipped,
            "taken_test" : taken_test,
        }
        return render(request,"tester/take_test/take_test.html", ctx )

    else:
        the_test = Test.objects.get(pk = testid)
        question_set = Question.get_test_questions(the_test)
        this_question = None

        this_question = question_set[current_question_num]
        next_question_num = current_question_num + 1
        if len(question_set) < next_question_num:
            next_question = 999999

        the_answers = Answer.get_answers(this_question)

        taken_test = TakenTest.objects.create(score = 0, related_test = the_test, student = request.user.student)
        

        given_answer_form = GivenAnswerForm()

        answered_question = AnsweredQuestion(related_taken_test = taken_test, related_question = this_question)

        GivenAnswerFormSet = inlineformset_factory(
        AnsweredQuestion ,
        GivenAnswer,
        fields = ("checked",) ,
        labels = {"checked" : ""},
        can_delete_extra = False,
        extra =  len(the_answers))


        givenanswer_formset = GivenAnswerFormSet()

        a_ga_zipped = zip(the_answers, givenanswer_formset)

        ctx = {
            "quantity_of_questions" : len(question_set),
            "this_question": this_question,
            "next_question_num": next_question_num,
            "the_answers" : the_answers,
            "givenanswer_formset" : givenanswer_formset,
            "the_test" : the_test,
            "a_ga_zipped" : a_ga_zipped,
            "taken_test" : taken_test,
        }
        return render(request,"tester/take_test/take_test.html", ctx )

@allowed_users(allowed_groups = ["student"])
def show_result(request, taken_test_id):
    
    
    taken_test = TakenTest.objects.get(pk = taken_test_id)
    answered_questions = AnsweredQuestion.objects.filter(related_taken_test = taken_test)
    score = sum([1 if ans_question.correct else 0 for ans_question in answered_questions])
    q_amount = len(answered_questions)
    taken_test.score = score
    taken_test.status = AnsweredTask.EVAL
    taken_test.grade = int((score / q_amount)* 5) 
    taken_test.save()
    
    #delete excessive taken_test instance
    TakenTest.objects.filter(student = request.user.student, related_test = taken_test.related_test)[0].delete()
    
    
    
    ctx = {
    "taken_test":taken_test,
    "q_amount" : q_amount,
    }
    return render(request, "tester/take_test/show_result.html", ctx)

@allowed_users(allowed_groups = ["student"])
def show_result_table(request, taken_test_id):
    taken_test = TakenTest.objects.get(id = taken_test_id)
    answered_questions = AnsweredQuestion.objects.filter(related_taken_test =  taken_test)
    given_ans_arr2d = []
    for a_q in answered_questions:
        answers  = GivenAnswer.objects.filter(related_answered_question = a_q)
        given_ans_arr2d += [answers]

    the_test = taken_test.related_test
    questions = Question.objects.filter(related_test = the_test)
    ans_arr2d = []
    for q in questions:
        answers = Answer.objects.filter(related_question = q)
        ans_arr2d += [answers]

    all_zipped = zip(questions,ans_arr2d,given_ans_arr2d,answered_questions)

    ctx = {
    "taken_test" : taken_test,
    "answered_questions" : answered_questions,
    "given_ans_arr2d" : given_ans_arr2d,
    "the_test": the_test,
    "questions":questions,
    "ans_arr2d":ans_arr2d,
    "all_zipped" : all_zipped,
    }
    return render(request, 'tester/take_test/show_result_table.html', ctx)





def login_form(request):
    if request.user.is_authenticated:
        return redirect("ts_profile")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is None:
            user_form = UserForm()
            ctx = {
            'error' : "Invalid username or password",
            "user_form" : user_form,
            }
            return render(request, "login/login_form.html", ctx)
        else:
            login(request,user)
            ctx = {
                "user" : user,
            }
            if is_teacher(user): return redirect("ts_profile" )
            else:  return redirect("ts_profile" )


    else:
        user_form = UserForm()
        ctx = {
        "user_form" : user_form,
        }
        return render(request, "login/login_form.html", ctx)




def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login_form')
