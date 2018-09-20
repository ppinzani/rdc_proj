#Std Lib Import
#Core Django Import
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
#Third-party import
#Import from apps
from .forms import LoginForm

login_redirect = "/mercaderias/"


# Create your views here.
def user_login(request):
    if request.method == "POST":
        if 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect(login_redirect)
        else:
            login_form = LoginForm()
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect(login_redirect)
        else:
            login_form = LoginForm()

    template = 'usuarios/login.html'
    variables = {'login_form': login_form}

    return render(request, template, variables)


def user_logout(request):
    logout(request)
    return redirect('/')
