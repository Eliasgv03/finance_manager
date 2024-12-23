from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden")

        # Aquí se valida la contraseña con los validadores de Django
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(f"Contraseña inválida: {', '.join(e.messages)}")
        
        return password


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput , required=True)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['initial_balance']
