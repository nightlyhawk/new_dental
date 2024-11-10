from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserForm, LoginUserForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_urls:login')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("patients_urls:list-patients")
    else:
        form = LoginUserForm()
    
    return render(request, "signin.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('user_urls:login')