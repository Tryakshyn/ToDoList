from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import todo_task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Функция представления для главной страницы
def home(request):
    return render(request, 'home.html')


# Функция представления для регистрации нового пользователя
def signup(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html',{'form':UserCreationForm})

    else:
        # Обработка POST запроса для создания нового пользователя
        if request.POST['password1'] == request.POST['password2']:
            try:
                 user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                 user.save()
                 login(request,user)
                 return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'signupuser.html',{'form':UserCreationForm,'error':'username not found'})

        else:
            return render(request, 'signupuser.html',{'form':UserCreationForm,'error': 'password not same'})

# Функция представления для выхода пользователя из системы
@login_required
def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect(home)

# Функция представления для входа пользователя в систему
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html',{'form':AuthenticationForm,'error':'username not matching'})
        else:
            login(request,user)
            return redirect('currenttodos')
            

# Функция представления для отображения текущих задач пользователя
def currenttodos(request):
    todos = tasklist.objects.filter(user = request.user,datecompleted__isnull=True)
    return render(request, 'currenttodos.html',{'todos':todos})

# Функция представления для отображения завершенных задач пользователя
def completedtodo(request):
    todo = tasklist.objects.filter(user = request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'completedtodos.html',{'todos':todo})

# Функция представления для создания новой задачи пользователя
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html',{'form':todo_task})
    else:
        try:
            form = todo_task(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodo.html',{'form':todo_task,'error':'value exceed'})

# Функция представления для просмотра и изменения задачи пользователя
def viewtodo(request,todo_pk):
    todos = get_object_or_404(tasklist,pk=todo_pk,user=request.user)
    if request.method =='GET':
        todoform = todo_task(instance=todos)
        return render(request, 'viewtodo.html',{'todo':todos,'form':todoform})
    else:
        try:
            form = todo_task(request.POST,instance=todos)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'viewtodo.html',{'todos':todos,'form':todoform,'error':'value error'})

# Функция представления для завершения задачи пользователя
def completetodo(request,todo_pk):
    todos = get_object_or_404(tasklist,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.datecompleted = timezone.now()
        todos.save()
        return redirect('currenttodos')

# Функция представления для удаления задачи пользователя
@login_required
def deletetodo(request,todo_pk):
    todos = get_object_or_404(tasklist,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect('currenttodos')


