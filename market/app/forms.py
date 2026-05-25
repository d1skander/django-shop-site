from django import forms


class BaseForm(forms.Form):
    pass


class UserForm(BaseForm):
    username = forms.CharField(min_length=3, max_length=12)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=20)
