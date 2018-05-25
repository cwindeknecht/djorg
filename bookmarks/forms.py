from django import forms
from .models import Bookmark
from django.contrib.auth.models import User

class BookmarkForm(forms.ModelForm): 
	class Meta:
		model = Bookmark
		fields = ('url', 'name', 'notes')

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None,
        }
