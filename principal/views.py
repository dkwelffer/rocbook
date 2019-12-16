from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse


# Aux functions
def get_name(request):

    return "{name} {last_name}".format(
        name=request.user.first_name,
        last_name=request.user.last_name
    )


# Views
@login_required
def index(request):

    name = get_name(request)

    context = {'name': name}
    return render(request, 'principal/index.html', context)


def login_session(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('principal:index'))

        else:
            context = {'error': True}
            return render(request, 'principal/login.html', context)

    return render(request, 'principal/login.html', {})


def logout_session(request):

    logout(request)
    return redirect(reverse('principal:login'))
