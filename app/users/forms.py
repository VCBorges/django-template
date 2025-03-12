from typing import override

from django import forms

from app.core.exceptions import ValidationError
from app.core.forms import BaseForm

from allauth.account.forms import LoginForm, SignupForm
from allauth.account.models import EmailAddress


class UserLoginForm(LoginForm):
    @override
    def is_valid(self, *, raise_exception: bool = True) -> bool:
        valid = super().is_valid()

        if not valid and raise_exception:
            raise ValidationError(self.errors)

        return valid


class CreateUserForm(BaseForm, SignupForm):
    first_name = forms.CharField(required=True)

    normalized_fields_mapping = {
        'password1': 'password',
    }

    def clean_email(self):
        email = super().clean_email()
        if EmailAddress.objects.filter(email=email).exists():
            self.add_error(
                field='email',
                error=forms.ValidationError('This email is already in use.'),
            )
        return email
    
    
    def clean(self):
        cleaned_data = super().clean()
        del cleaned_data['password2']
        return cleaned_data


class UpdateUserView(BaseForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    height = forms.FloatField(required=True)
    weight = forms.FloatField(required=True)


class EmailVerificationForm(BaseForm): ...
