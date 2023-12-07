from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('send-email-verification/', lambda request: render(request, 'account/send_email_verification.html'),
         name='send-email-verification'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile-management/', profile_management_view, name='profile-management'),
    path('delete-user/', delete_user_view, name='delete-user'),
]
