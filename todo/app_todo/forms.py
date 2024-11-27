from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


#class CustomLoginForm(AuthenticationForm):
#    username = forms.CharField(label="Имя пользователя", max_length=100)
#    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
