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









class Main:
    def homepage(request):
        return render(request,"homepage/homepage.html",{})




class Student_views:

    @allowed_users(allowed_groups = ["student"])
    def s_profile(request):
        return render(request,"student_views/s_profile.html",{})

    @allowed_users(allowed_groups = ["student"])
    def s_tasks(request):
        ctx = {}
        return render(request, "student_views/s_statistics.html", ctx)

    @allowed_users(allowed_groups = ["student"])
    def s_subjects(request):
        ctx = {}
        return render(request, "student_views/s_subjects.html", ctx)

    @allowed_users(allowed_groups = ["student"])
    def s_statistics(request):
        ctx = {}
        return render(request, "student_views/s_tasks.html", ctx)


class Teacher_views:
    @allowed_users(allowed_groups = ["teacher"])
    def t_profile(request):
        ctx = {}
        return render(request,"teacher_views/t_profile.html",ctx)

    @allowed_users(allowed_groups = ["student"])
    def t_tasks(request):
        ctx = {}
        return render(request,"teacher_views/t_statistics.html",ctx)

    @allowed_users(allowed_groups = ["teacher"])
    def t_subjects(request):
        print(request.user.teacher)
        print("data")
        subjects = Subject.objects.all().filter(teacher = request.user.teacher)
        ctx = {
        "subjects":subjects,
        }
        return render(request,"teacher_views/t_subjects.html",ctx)

    @allowed_users(allowed_groups = ["teacher"])
    def t_statistics(request):



        ctx = {}

        return render(request,"teacher_views/t_tasks.html",{})




class TestList(ListView):
    paginate_by = 10
    model = Test
    template_name = "tester/storage/test_list.html"




class Tester:
    def create_test(request):
        if request.method == "POST":
            form_result = TestForm(request.POST,request.FILES)
            if form_result.is_valid():
                test_instance = form_result.save()
                return redirect('create_questions', test_instance.pk)

        form_test = TestForm()
        ctx = {
            "form_test": form_test,
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

    def geturl(request, testid):

        the_test = Test.objects.get(id = testid)

        questions = Question.objects.filter(related_test=the_test)
        if len(questions)==0:
            the_test.delete()
            return render(request, "tester/create_test/cant_create_test.html", {})

        path = reverse(Tester.start_a_test, args = [testid])
        yoururl = str(request.META["HTTP_HOST"])  + str(path)

        the_test.link = yoururl
        the_test.save()

        ctx = {
        "testid":testid,
        "yoururl": yoururl,
        }

        return render(request, "tester/create_test/geturl.html", ctx)



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

            #formset = GivenAnswerFormSet(request.POST)




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




class Login:
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
                t = Teacher.objects.get(user = user)
                if t: return redirect("t_profile" )
                else:  return redirect("s_profile" )
                # if t: return render(request, "teacher_views/t_profile.html", ctx)
                # else:  return render(request, "student_views/s_profile.html", ctx)

        else:
            user_form = UserForm()
            ctx = {
            "user_form" : user_form,
            }
            return render(request, "login/login_form.html", ctx)




    def log_out(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(Main.homepage)
