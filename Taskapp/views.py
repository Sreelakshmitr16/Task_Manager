from django.shortcuts import render,redirect
from django.views.generic import View
from Taskapp.forms import TaskForm
from Taskapp.models import Task
from Taskapp.forms import RegistrationForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Count
from Taskapp.decorators import signin_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache
decs=[signin_required,never_cache]

# Create your views here.

# -----------TASK CREATE VIEW-----------
# url:localhost:8000//Taskapp/tasks/add/
# method:get,post

@method_decorator([signin_required,never_cache],name='dispatch')
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,'task_add.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            form.instance.user_object=request.user
            form.save()
            messages.success(request,'task added successfully')
            return redirect('task-list')
        messages.error(request,'task added failed')
        return render(request,'task_add.html',{'form':form})
    

#-------------TASK LISTING------------:
# url:localhost:8000/Taskapp/tasks/all/
# method:get

@method_decorator([signin_required,never_cache],name='dispatch')
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        qs=Task.objects.filter(user_object=request.user)
        group_by_qs=Task.objects.filter(
            user_object=request.user,
            date__month=cur_month,
            date__year=cur_year
            ).values('status').annotate(status_count=Count('status'))
        print(group_by_qs)
        return render(request,"task_list.html",{"data":qs,'status_count':group_by_qs})


#-----------TASK UPDATE-----------------------:
    # url:localhost:8000/Taskapp/tasks/{id}/change/
    # method:get,post

@method_decorator(decs,name='dispatch')
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        task_object=Task.objects.get(id=id)
        form=TaskForm(instance=task_object)
        return render(request,"task_edit.html",{'form':form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        task_object=Task.objects.get(id=id)
        form=TaskForm(request.POST,instance=task_object)
        if form.is_valid():
            form.save()
            return redirect('task-list')
        return render(request,"task_edit.html",{'form':form})


#------------TASK DELETE--------------------------:
    # url:localhost:8000/Taskapp/tasks/{id}/remove/
    # method:get

@method_decorator(decs,name='dispatch')
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Task.objects.get(id=id).delete()
        messages.success(request,'task deleted successfully')
        return redirect('task-list')


#------------TASK DETAIL------------------:
    # url:localhost:8000/Taskapp/tasks/{id}/
    # method:get

@method_decorator(decs,name='dispatch')
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Task.objects.get(id=id)
        return render(request,'task_detail.html',{'data':qs})
    

# --------------USER CREATE VIEW(SIGNUP VIEW)-------------
    # url:localhost:8000/budget/register/
    # method:get,post

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{'form':form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'registered  successfully')
            return redirect('signin')
        messages.error(request,'registration failed')
        return render(request,"register.html",{'form':form})


# -------SIGNIN VIEW(LOGIN VIEW)--------
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            uname=data.get('username')
            pwd=data.get('password')
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print('login success')
                messages.success(request,'login success')
                return redirect('task-list')
        messages.error(request,'login failed')
        return render(request,"login.html",{'form':form})
    
# ----------SIGNOUT VIEW(LOGOUT VIEW)--------
@method_decorator([signin_required,never_cache],name='dispatch')
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'logout successfully')
        return redirect('signin')
            

