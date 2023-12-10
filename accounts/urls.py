from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy

from .views import (dashboard_view, delete_user_view, login_view, logout_view,
                    profile_management_view, register_view)

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('send-email-verification/', lambda request: render(request, 'accounts/email/send_email_verification.html'),
         name='send-email-verification'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile-management/', profile_management_view, name='profile-management'),
    path('delete-user/', delete_user_view, name='delete-user'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password/password_reset.html',
        email_template_name='accounts/password/password_reset_email.html',
        success_url=reverse_lazy('accounts:password-reset-done')), name='password-reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password/password_reset_done.html'), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password-reset-complete')), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password/password_reset_complete.html'), name='password-reset-complete'),
]
