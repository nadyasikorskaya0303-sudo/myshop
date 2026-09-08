from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с дополнительными полями"""
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="О себе")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'bio', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                bio=self.cleaned_data.get('bio', '')
            )
        return user


class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля"""
    
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'avatar': forms.FileInput(),
        }
        labels = {
            'bio': 'О себе',
            'phone': 'Телефон',
            'avatar': 'Аватар',
        }
