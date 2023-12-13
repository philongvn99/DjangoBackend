from django import forms
from django.core.validators import RegexValidator, EmailValidator


loginValidator = [
    RegexValidator(
        r"^[a-zA-Z0-9]{7,32}$",
        message="Input must be Alphanumeric with maximum length 31",
    ),
]

phoneValidator = [
    RegexValidator(
        r"^\+84\d{9}$",
        message=("Phone number format: 9 digits following +84 (VIE)"),
    )
]

nameValidator = [
    RegexValidator(
        r"^[a-zA-Z]{2,}( [a-zA-Z]+)*$",
        message=("Phone number format: 9 digits following +84 (VIE)"),
    )
]


class LoginInfoForm(forms.Form):
    email = forms.CharField(min_length=8, max_length=32, validators=[EmailValidator])
    password = forms.CharField(min_length=7, max_length=32, validators=loginValidator)

class UserInfoForm(forms.Form):
    ROLES = [
        ("A", "Admin"),
        ("S", "Supporter"),
        ("U", "User"),
        ("G", "Guest"),
    ]

    def is_privileged(self):
        return self.role in {"A", "S"}

    def is_visible(self):
        return self.role in {"A", "S", "U"}

    username = forms.CharField(min_length=8, max_length=32, validators=loginValidator)
    password = forms.CharField(min_length=8, max_length=32, validators=loginValidator)
    phone = forms.CharField(min_length=8, max_length=40, validators=phoneValidator)
    name = forms.CharField(min_length=8, max_length=40, validators=nameValidator)
    email = forms.CharField(min_length=8, max_length=40)
    license = forms.CharField(initial="00Z0-00000", min_length=8, max_length=10)
    role = forms.ChoiceField(choices=ROLES, initial="U")
    