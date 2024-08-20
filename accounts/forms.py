from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)

User=get_user_model


class UserLoginform(forms.Form):
    username = forms.CharField(label='Enter Your Email')
    password = forms.CharField(widget=forms.PasswordInput,label='Enter Your Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("This user does not exist or the password is incorrect.")
            if not user.is_active:
                raise forms.ValidationError("This user is not active.")
        return cleaned_data