from django import forms
from Taskapp.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=('date','user_object')
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            
            'status':forms.Select(attrs={'class':'form-control'}),
            }
        
class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','Placeholder':"Enter password"}),label='Password')
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','Placeholder':"Confirm password"}),label='Confirm Password')
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','Placeholder':"Enter Username"}),
            'email':forms.TextInput(attrs={'class':'form-control','Placeholder':"Enter email"}),
            

        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','Placeholder':"Enter username"}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','Placeholder':"Enter password"}))
