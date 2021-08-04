from app import models
from app.models import Customer
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm, AuthenticationForm, UsernameField,PasswordChangeForm,PasswordResetForm
from django import forms
from django.forms import fields, widgets
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _


class Userupdateform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'})}

class CustomerProfile(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id','name','mobile','locality','city','state','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'mobile':forms.NumberInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        'user':forms.TextInput(attrs={'class':'form-control'})}


class user_signup(UserCreationForm):
    password1= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields=['username','email']
        labels={'username':"Username",'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'})}
    

class loginform(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
    password=forms.CharField(label=_('Password'),strip=False, widget=forms.PasswordInput(attrs=
    {'autofocus': True, 'class':'form-control'}))


class Change_password(PasswordChangeForm):
    old_password= forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1= forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User

class Reset_pass(PasswordResetForm):
     email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

        
class Mysetpassword(SetPasswordForm):
    new_password1= forms.CharField(label='New Password',
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',
    widget=forms.PasswordInput(attrs={'class':'form-control'}))

    # new_password1 = forms.CharField(
    #     label=_("New password"),
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    #     strip=False,
    #     help_text=password_validation.password_validators_help_text_html(),
    # )

    # new_password2 = forms.CharField(label=_("New password confirmation"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    # )



  
    
        