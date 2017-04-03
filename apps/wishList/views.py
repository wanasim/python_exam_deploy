from django.shortcuts import render, redirect
from .models import Item
from ..loginReg.models import User
from django.contrib import messages

def dashboard(request):
    #check for user session
    if 'id' in request.session:
        name = User.objects.get(id=request.session['id'])
        current_user = Item.objects.filter(user_of_item__id=request.session['id'])
        not_user = Item.objects.exclude(user_of_item__id=request.session['id'])
        items = Item.objects.all()

        context={
            "items": items,
            "current_user": current_user,
            "not_user":not_user,
            "name": name,
        }
        return render(request, 'wishList/dashboard.html', context)
    return redirect('loginReg:index')


def addItem(request): #routes to addItem html page
    if 'id' in request.session:
        return render(request, 'wishList/addItem.html')
    return redirect('loginReg:index')


def createItem(request): #creates item
    #check for user session
    if 'id' in request.session:
        valid, response, info = Item.objects.createItem(request.POST)

        if not valid:
            for error in response:
                messages.error(request, error)
            return redirect('wishList:addItem')
        return redirect('wishList:dashboard')
    return redirect('loginReg:index')


def itemInfo(request, id):
    if 'id' in request.session:
        all_users = Item.objects.getUsers(id)


        print "ALL USERS", all_users

        context = {
            "item_name" : Item.objects.get(id=id),
            "all_users" : all_users,
        }
        return render(request, 'wishList/itemInfo.html', context)
    return redirect('loginReg:index')


def removeItem(request, id):
    if 'id' in request.session:
        user_id = request.session['id']
        remove_item_message = Item.objects.removeItem(user_id,id)
        return redirect('wishList:dashboard')
    return redirect('loginReg:index')


def deleteItem(request, id):
    if 'id' in request.session:
        Item.objects.deleteItem(id)
        return redirect('wishList:dashboard')
    return redirect('loginReg:index')


def addToList(request, id):
    #SWITCH TO HAVE IN DB
    if 'id' in request.session:
        user_id = request.session['id']
        add_item = Item.objects.addToList(user_id, id)

        return redirect('wishList:dashboard')
    return redirect('loginReg:index')
