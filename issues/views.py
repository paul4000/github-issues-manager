from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")


@login_required
def homepage(request):
    return render(request, 'issues/homepage.html')


def logout(request):
    auth_logout(request)
    return redirect('/login')