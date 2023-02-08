'''
파일명 : forms.py
설명 : 회원가입 form
생성일 : 2023/02/06
생성자 : ckair
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label = "이메일")

    class Meta:
        model = User
        # password1 , password2 (비밀번호 1을 제대로 입력했는지 대조하기 위한 값)
        fields = ('username','password1','password2','email')