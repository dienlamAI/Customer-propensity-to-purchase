# files.py
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control form-control-user'}))
    last_name = forms.CharField(max_length=100, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control form-control-user'}))
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control form-control-user'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email Address',
                                                           'class': 'form-control form-control-user',
                                                           'type': 'email'}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control form-control-user',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password'}))
    password_2 = forms.CharField(required=True, label='Confirm Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password',
                                                                   'class': 'form-control form-control-user',
                                                                   'data-toggle': 'password',
                                                                   'id': 'password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is taken")
        return username

class PasswordChangeForm1(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Current Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'id_old_password',
                                                                  }))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'New password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'id_new_password1',
                                                                  }))
    new_password2 = forms.CharField(required=True, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'id_new_password2',
                                                                  }))
    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("The old password is incorrect")
        return old_password

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
class LoginForm(forms.Form):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'type': 'text',
            'placeholder': 'Username',
            'autofocus': True,
            'required': 'required'
        })
    )
    
    password = forms.CharField(label='', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'name': 'password',
            'placeholder': 'Password',
            'required': 'required'
        }),
    )

    remember_me = forms.BooleanField(required=False, label='Remember Me')

    def __init__(self, *args, **kwargs):
        kwargs.pop('request', None)
        super().__init__(*args, **kwargs)