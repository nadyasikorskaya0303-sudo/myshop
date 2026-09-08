from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'myauth'

urlpatterns = [
    # Аутентификация
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Cookies и сессии
    path('cookie/get/', views.get_cookie_view, name='cookie_get'),
    path('cookie/set/', views.set_cookie_view, name='cookie_set'),
    path('session/get/', views.get_session_view, name='session_get'),
    path('session/set/', views.set_session_view, name='session_set'),
    
    # Профиль (CBV)
    path('about-me/', views.AboutMeView.as_view(), name='about_me'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('users/<int:pk>/update/', views.AdminUpdateProfileView.as_view(), name='admin_update_profile'),
]
