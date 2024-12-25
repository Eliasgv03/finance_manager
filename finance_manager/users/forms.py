from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña",
        help_text="Debe contener al menos 8 caracteres, no ser completamente numérica, y cumplir con las políticas de seguridad."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        """Valida que las contraseñas coincidan y cumple con las reglas de Django."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        
        # Validación de la contraseña según las políticas de Django
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)

        return cleaned_data

    def save(self, commit=True):
        """Cifra la contraseña antes de guardar el usuario."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Cifra la contraseña
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput , required=True)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['initial_balance']
