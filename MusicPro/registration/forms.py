from django import forms
from django.views.generic.edit import FormView
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# tipo_cuenta_choices = (
#     ("1", "cliente"),
#     ("2", "admin"),
# )

# class SignUpFormWithEmail(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=254)
#     tipo_cuenta = forms.ChoiceField(choices = tipo_cuenta_choices)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'tipo_cuenta')

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("El email ya está registrado, prueba con otro.")
#         return email

class CustomSignUpForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    tipo_cuenta = forms.ChoiceField(choices=[('admin', 'Administrador'), ('client', 'Cliente')])

    def clean_password(self):
        return self.cleaned_data.get('password')