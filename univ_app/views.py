from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.views.generic import ListView
from .decorators import allowed_users
from .utils import get_task, is_teacher
from django.contrib import messages











def homepage(request):
    return render(request,"homepage/homepage.html",{})






#student
# @allowed_users(allowed_groups = ["student"])
# def s_profile(request):
#     return render(request,"student_views/s_profile.html",{})

@allowed_users(allowed_groups = ["student"])
def s_tasks(request):
    ctx = {}
    return render(request, "student_views/s_statistics.html", ctx)

# @allowed_users(allowed_groups = ["student"])
# def s_subjects(request):
#     ctx = {}
#     return render(request, "student_views/s_subjects.html", ctx)

@allowed_users(allowed_groups = ["student"])
def s_statistics(request):
    ctx = {}
    return render(request, "student_views/s_tasks.html", ctx)




#Teacher







@allowed_users(allowed_groups = ["teacher"])
def t_task_answers(request):
    ctx = {
    }
    return render(request,"teacher_views/t_student_answers.html",ctx)



@allowed_users(allowed_groups = ["teacher"])
def t_choose_task_type(request, subject_id):
    return render(request,"teacher_views/t_choose_task_type.html",{"subject_id":subject_id})


@allowed_users(allowed_groups = ["teacher"])
def t_create_task(request, subject_id = None, task_type=None):
    teacher = request.user.teacher
    form = CommonTaskForm()
    print(task_type)
    if request.method == "POST":
        if task_type == "CommonTask":
            form = CommonTaskForm(request.POST, request.FILES)
            if form.is_valid():
                common_task = form.save(commit=False)
                common_task.created_by = teacher
                common_task.subject = Subject.objects.get(id = subject_id)
                common_task.save()
                messages.success(request, "Задание было успешно создано и опубликовано")
                return redirect('ts_subject', subject_id)

        if task_type == "InfoTask":
            form = InfoTaskForm(request.POST, request.FILES)
            if form.is_valid():
                info_task = form.save(commit=False)
                info_task.created_by = teacher
                info_task.subject = Subject.objects.get(id = subject_id)
                info_task.save()
                messages.success(request, "Информация была успешно опубликована")
                return redirect('ts_subject', subject_id)

        form = CommonTaskForm(request.POST)
        ctx = {
        "form":form,
        "subject_id":subject_id,
        }
        return render(request, "teacher_views/t_create_common_task.html", ctx)





    if task_type == "Commontask":
        pass
    elif task_type == "Test":
        return redirect("create_test", subject_id = subject_id)
    elif task_type == "InfoTask":
        form = InfoTaskForm()
    ctx = {
    "form":form,
    "subject_id":subject_id,
    }
    return render(request,"teacher_views/t_create_common_task.html",ctx)


@allowed_users(allowed_groups = ["teacher"])
def t_student_answers(request):

    ctx = {

    }
    return render(request,"teacher_views/t_student_answers.html",ctx)

@allowed_users(allowed_groups = ["teacher"])
def t_statistics(request):
    ctx = {}
    return render(request,"teacher_views/t_statistics.html",{})



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
def ts_task(request, task_type, task_id):
    task = get_task(task_type, task_id)
    ctx = {
    "task":task
    }
    return render(request,"mutual_views/ts_task.html",ctx)




#Tester
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

def finish_test_creation(request, testid):
    test = Test.objects.get(id = testid)
    if Question.objects.filter(related_test=test).count() == 0:
        the_test.delete()
        return render(request, "tester/create_test/cant_create_test.html", {})
    return redirect("ts_subject", test.subject.id)



def start_a_test(request, testid):
    the_test = Test.objects.get(id = testid)
    ctx = {
    "the_test":the_test,
    }
    return render(request,"tester/take_test/start_a_test.html", ctx )


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
            next_question = question_set[current_question_num] #выход за пределы индекса
            print(next_question)
            if next_question is not None:
                next_answers = Answer.objects.filter(related_question = next_question) #cannot unpack non-iterable
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

        taken_test = TakenTest.objects.create(score = 0, related_test = the_test)

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


def show_result(request, taken_test_id):
    taken_test = TakenTest.objects.get(pk = taken_test_id)
    answered_questions = AnsweredQuestion.objects.filter(related_taken_test = taken_test)
    taken_test.score = sum([1 if ans_question.correct else 0 for ans_question in answered_questions])
    taken_test.save()
    q_amount = len(answered_questions)
    ctx = {
    "taken_test":taken_test,
    "q_amount" : q_amount,
    }
    return render(request, "tester/take_test/show_result.html", ctx)


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
    return redirect('homepage')
