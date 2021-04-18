from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, PasswordInput, Form
from django.contrib.auth.password_validation import validate_password


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PasswordChangeForm(Form):
    old_password = CharField(widget=PasswordInput)
    new_password = CharField(widget=PasswordInput,
                             validators=[validate_password])
    confirm_password = CharField(widget=PasswordInput)

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        new_password = cleaned_data.get('new_password')

        if new_password != confirm_password:
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, user):
        if user.check_password(self.cleaned_data['old_password']):
            user.set_password(self.cleaned_data['new_password'])
            user.save()
