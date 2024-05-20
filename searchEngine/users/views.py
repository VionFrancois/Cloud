from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

def register_view(request):
    if request.method == 'POST':
        # Create a form with the data from the request
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            # Display the non valid fields
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # Create a form with the data from the request
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # Login the user and redirect to the application page
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def index_view(request):
    return redirect('/searchClient/index')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
