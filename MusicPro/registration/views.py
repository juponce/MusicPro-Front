# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpFormWithEmail
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'registration/signup.html'

#     def get_success_url(self):
#         return reverse_lazy('login') + '?register'

class SignUpView(CreateView):
    form_class = SignUpFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    # def get_form(self, form_class=None):
    #     form = super(SignUpView, self).get_form()
