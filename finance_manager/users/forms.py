from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required'
        }),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label="Password",
        help_text="Must be at least 8 characters long and meet security requirements."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput , required=True)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['initial_balance' , 'default_currency']
