from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.contrib.auth import logout as auth_logout, login as auth_login,\
    authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages

from .forms import RegistrationForm


class Registration(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        form.save()
        self.success_url = self.request.META.get('HTTP_REFERER')
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'])
        auth_login(self.request, user)
        # Передача сообщения через сессию в `request`
        self.request.session['success_message'] = \
            'Регистрация прошла успешно'
        return super(Registration, self).form_valid(form)


class Loginauth(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            redirectpath = request.META.get('HTTP_REFERER')
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(redirectpath)
            else:
                if not username and not password:
                    return HttpResponseRedirect(redirectpath)
                else:
                    '''Передача ссобщения в шаблон путём `messages`, 
                        использование куки (либо сесий),
                        также следует выставить переменную 
                        `MESSAGE_STORAGE` в settings.py'''
                    messages.add_message(
                        request, messages.ERROR,
                        'Проверьте корректность <br> полей  логин и пароль.')
                    return HttpResponseRedirect(redirectpath)
        return super(Loginauth, self).dispatch(request, *args, **kwargs)


class Logoutauth(RedirectView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        self.url = request.META.get('HTTP_REFERER')
        return super(Logoutauth, self).get(request, *args, **kwargs)
