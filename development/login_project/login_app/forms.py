from django import forms
from .models import Registrations_data,Post

class Reg_form(forms.ModelForm):
    class Meta:
        model=Registrations_data
        fields='__all__'


class Login_form(forms.ModelForm):
    class Meta:
        model=Registrations_data
        fields=['email','password'] 


class  post_form(forms.ModelForm):
    class Meta:
        model=Post
        fields=[
            'title',
            'content'
        ]              
       