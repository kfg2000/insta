from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content',]

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'profilePic')

        widgets = {
            'birth_date': forms.DateInput(attrs={"type": "date"}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CommentForm(forms.ModelForm):
    blob = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        model = Comment
        fields = ['blob']
