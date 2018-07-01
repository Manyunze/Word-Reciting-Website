# coding:utf-8


from django import forms
from .models import Vocabulary
from django.contrib.auth.models import User
import re


class UserForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    daily_words = forms.IntegerField(min_value=1, max_value=1000, initial=50)
    try:
        vocabularys = Vocabulary.objects.all()
        # print(vocabularys)
        choices = tuple([(v.id, v.name) for v in vocabularys])
        vocabulary = forms.ChoiceField(choices=choices,
                                       widget=forms.widgets.Select())
    except:
        # 防止初始化数据库的时候，没有vocabulary会报错
        choices = (1, 1)
        vocabulary = forms.ChoiceField(choices=choices,
                                       widget=forms.widgets.Select())

    def clean_username(self):
        '''验证用户输入的用户名的合法性'''
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('用户名中只能包含字母、数字和下划线')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('用户名已存在！')

    def clean_password2(self):
        '''验证用户两次输入的密码一致性'''
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('两次输入的密码不匹配')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class SettingsForm(forms.Form):
    daily_words = forms.IntegerField(
        min_value=1, max_value=1000)
    try:
        vocabularys = Vocabulary.objects.all()
        # print(vocabularys)
        choices = tuple([(v.id, v.name) for v in vocabularys])
        vocabulary = forms.ChoiceField(choices=choices,
                                       widget=forms.widgets.Select())
    except:
        choices = (1, 1)
        vocabulary = forms.ChoiceField(choices=choices,
                                       widget=forms.widgets.Select())


class NoteForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    shared = forms.BooleanField(required=False, initial=True)
