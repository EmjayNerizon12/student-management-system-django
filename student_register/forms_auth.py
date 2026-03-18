from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .form_mixins import StyledFieldsMixin


class LoginForm(StyledFieldsMixin, AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
