from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import time

# Create your views here.
def index(request):
    return render(request, 'loginReg/index.html')

def register(request):
    #User account
    valid, message, info = User.objects.register(request.POST)
    print valid, message
    if not valid:
        for error in message:
            messages.error(request, error)
        return redirect('loginReg:index')
    print request.POST['name']
    request.session['name'] = info.name
    request.session['id']=info.id
    context = {
        "user" : request.POST['name'],
    }
    return redirect('wishList:dashboard') #EDITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTt

def login(request):
    valid, message, info = User.objects.login(request.POST)
    print valid, message
    if not valid:
        for error in message:
            messages.error(request, error)
        return redirect('loginReg:index')

    request.session['name'] = info.name
    request.session['id']=info.id
    context = {
        "user" : info,
    }
    return redirect('wishList:dashboard') 


def logout(request):
    request.session.clear()
    return redirect('loginReg:index')
