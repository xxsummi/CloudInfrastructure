from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username=forms.CharField(label="Username", max_length=20)
	password=forms.CharField(label="Password", max_length=20)

class AddTaskForm(forms.Form):
    task_name = forms.CharField(label="Task Name", max_length=50)
    description = forms.CharField(label="Description", max_length=200)

class UpdateTaskForm(forms.Form):
    task_name = forms.CharField(label="Task Name", max_length=50)
    description = forms.CharField(label="Description", max_length=200)
    status = forms.CharField(label="Status", max_length=50)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
