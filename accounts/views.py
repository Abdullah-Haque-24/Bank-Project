from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(user, subject, template):
    try:
        message = render_to_string(template, {'user': user})
        email = EmailMultiAlternatives(subject, '', to=[user.email])
        email.attach_alternative(message, "text/html")
        email.send()
    except Exception as e:
        print(f"Error sending email: {e}")

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(View):  
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            send_email(self.request.user, "Profile Update Message", "accounts/mail.html")
            return redirect('profile')
        
        return render(request, self.template_name, {'form': form})
    

class PasswordChangeView(View):
    template_name = 'accounts/change_password.html'

    def get(self, request):
        password_form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'password_form': password_form})

    def post(self, request):
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully.')
            send_email(self.request.user, "Password Update Message", "accounts/pass_change_mail.html")
            return redirect('profile')
        
        return render(request, self.template_name, {'password_form': password_form})
    
    