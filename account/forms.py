from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    password_again =  forms.CharField(label="Password again", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email", max_length=40, widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ('username', 'password')
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # self.fields['comment'].widget.attrs['placeholder'] = self.fields['email'].label or 'email@address.nl'

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        pwd = cleaned_data.get('password')
        pwd2 = cleaned_data.get('password_again')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')


        if pwd and pwd2:
            if not pwd == pwd2:
                self.add_error(
                    "password_again",
                    "The passwords must be the same!"
                )

        if username:
            if User.objects.filter(username=username).exists():
                self.add_error(
                    "username",
                    "This username is already used bu another user!"
                )

        if email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    "email",
                    "This email is already used bu another user!"
                )


        return cleaned_data
