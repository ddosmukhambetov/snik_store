from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email

from .forms import UserCreateForm, UserLoginForm, UserUpdateForm

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data['email']
            user_username = form.cleaned_data['username']
            user_password = form.cleaned_data['password2']
            user = User.objects.create_user(user_username, user_email, user_password)
            user.is_active = False
            send_email(user)
            return redirect('accounts:send-email-verification')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/register_login/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('accounts:login')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/register_login/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('products')


@login_required(login_url='accounts:login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard/dashboard.html')


@login_required(login_url='accounts:login')
def profile_management_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/dashboard/profile_management.html', {'form': form})


@login_required(login_url='accounts:login')
def delete_user_view(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('products')
    else:
        return render(request, 'accounts/dashboard/delete_user.html')
