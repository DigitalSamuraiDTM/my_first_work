from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from subs.models import Users_data_question

def view_404(request):
    return render(request, 'subs/404NotFound.html')


def view_500(request):
    return render(request,'subs/500serverError.html')




def register(request):
    return render(request, 'subs/register.html')


def login(request):
    return render(request, 'subs/login.html')


def index(request):
    baton = 10
    out = {'baton': baton}
    a = 'subs/index.html'
    return render(request, a, out)


def start_quest(request):
    return render(request, 'subs/test_filips/start.html')


def rezults(request):
    return render(request, 'subs/test_filips/rezults.html')


def FilipsTest(request):
    return render(request, 'subs/test_filips/test.html')


def zero(request):
    return render(request, 'subs/zero.html')


def signup(request):
    login = request.POST.get("login", False)
    Lname = request.POST.get("last_name", False)
    Fname = request.POST.get("first_name", False)
    mail = request.POST.get("mail", False)
    password = request.POST.get("password", False)
    repeat_password = request.POST.get("repeat_password", False)

    if password == repeat_password:
        registr = User.objects.create_user(email=mail, username=login, password=password, first_name=Fname, last_name=Lname)
        registr.save()
        registr = Users_data_question(login=login, true_choice=0, bad_choice=0, reiteration_test=0)
        registr.save()
        return HttpResponseRedirect('/main')
    elif password != repeat_password:
        return HttpResponseRedirect('/')


def check_login(request):
    login = request.GET.get('login', False)
    user = User.objects.values_list('username', flat=True)  # выборка значений столбца из базы данных
    if login not in user:
        return HttpResponse('good', content_type='text/html')
    else:
        return HttpResponse('bad', content_type='text/html')


def check_mail(request):
    mail = request.GET.get('mail', False)
    user_mail = User.objects.values_list('email', flat=True)
    if mail not in user_mail:
        return HttpResponse('good', content_type='text/html')
    else:
        return HttpResponse('bad', content_type='text/html')


def login_user(request):
    login = request.POST.get('login_log', False)
    password = request.POST.get('password_log', False)
    user = auth.authenticate(username=login, password=password) #проверка существования юзера с логином и паролем
    if user is not None: #если юзер существует
        auth.login(request, user) #логин
        return HttpResponseRedirect('/main/', request)
    else:
        login_error = {'login_error': 'Такого пользователя не существует или ваш пароль неверен'} #иначе выводим ошибку
        return render_to_response('subs/login.html', login_error) #отправляем


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/main/', request)


def work(request):
    return render(request, 'subs/work.html')


def save_additional_data(request):
    true_choice = int(request.POST.get('true_choice', False))
    bad_choice = int(request.POST.get('bad_choice', False))
    login = request.POST.get('login', False) #пример изменений данных в бд
    additional = Users_data_question.objects.get(login=login)  #выбираем объект с именем login
    additional.bad_choice+= bad_choice #производим изменения с этими полями
    additional.true_choice += true_choice
    additional.reiteration_test +=1
    additional.save() #сохраняем изменения sql запросом


    return rezults(request)


def profile(request):
    return render(request, 'subs/profile.html')