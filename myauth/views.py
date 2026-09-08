from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile


# ============================================================
# 1. АУТЕНТИФИКАЦИЯ
# ============================================================

class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:login')


# ============================================================
# 2. РАБОТА С COOKIES И СЕССИЯМИ
# ============================================================

def get_cookie_view(request):
    cookie_value = request.COOKIES.get('my_cookie', 'Нет значения')
    return render(request, 'myauth/cookie_get.html', {'cookie_value': cookie_value})


def set_cookie_view(request):
    response = render(request, 'myauth/cookie_set.html')
    response.set_cookie('my_cookie', 'Hello, Cookie!', max_age=3600)
    return response


def get_session_view(request):
    session_value = request.session.get('my_session_key', 'Нет значения')
    return render(request, 'myauth/session_get.html', {'session_value': session_value})


def set_session_view(request):
    request.session['my_session_key'] = 'Hello, Session!'
    return render(request, 'myauth/session_set.html')


# ============================================================
# 3. ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (CBV)
# ============================================================

class AboutMeView(UpdateView):
    model = Profile
    fields = ('avatar',)
    template_name = 'myauth/about_me.html'
    success_url = reverse_lazy('myauth:about_me')
    
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'myauth/update_profile.html'
    success_url = reverse_lazy('myauth:about_me')
    
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def test_func(self):
        """Проверяет, может ли пользователь редактировать свой профиль"""
        if self.request.user.is_staff:
            return True
        profile = self.get_object()
        return profile.user == self.request.user


class UserListView(ListView):
    model = User
    template_name = 'myauth/user_list.html'
    context_object_name = 'users'


class UserProfileView(DetailView):
    model = User
    template_name = 'myauth/user_profile.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = Profile.objects.get_or_create(user=self.object)
        context['profile'] = profile
        return context


class AdminUpdateProfileView(UserPassesTestMixin, UpdateView):
    """Редактирование профиля пользователя (только для staff)"""
    model = Profile
    form_class = ProfileForm
    template_name = 'myauth/update_profile.html'
    
    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        profile, created = Profile.objects.get_or_create(user=user)
        return profile
    
    def test_func(self):
        """Только staff может редактировать профили других пользователей"""
        return self.request.user.is_staff
    
    def get_success_url(self):
        return reverse_lazy('myauth:user_profile', kwargs={'pk': self.kwargs['pk']})
