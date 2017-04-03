from __future__ import unicode_literals
from django.db import models
from ..loginReg.models import User

class ItemManager(models.Manager):
    def createItem(request, data):
        error=[]
        if not len(data['item_name']) > 3:
            error.append("Please enter an item name that is greater than 3 characters")
        if error:
            return (False, error, False)

        print "USER ID=", data['user_id']

        try:
            item_exist = Item.objects.get(item_name=data['item_name'])
            if item_exist:
                error.append("Item already exists")
                return (False, error, False)
        except:
            print "It is indeed a new item"
            pass

        #Get/create user and item instances
        user_info = User.objects.get(id=data['user_id'])
        user_info.item_of_user.create(item_name=data['item_name'], creator=user_info)
        user_info.save()

        #--------------------------------------------------------
        # Another way to create item:
        # new_item = Item.objects.create(item_name=data['item_name'])
        # new_item.save()
        # new_item.user_of_item.add(user_info)


        return (True, "Succesful registration to Wish List!", user_info)


    def getUsers(request, id):
        all_users = User.objects.filter(item_of_user=id)
        return all_users

    def addToList(request, user_id, item_id):
        user_info = User.objects.get(id=user_id)
        curr_item = Item.objects.get(id = item_id)
        print "Current item name", curr_item.item_name

        user_info.item_of_user.add(curr_item)
        user_info.save()

    def removeItem(request, user_id, item_id):
        user_info = User.objects.get(id=user_id)
        item = Item.objects.get(id=item_id)
        item.user_of_item.remove(user_info)
        item.save()
        return "Successfully removed item"

    def deleteItem(request, item_id):
        Item.objects.get(id=item_id).delete()


#Models
class Item(models.Model):
    item_name = models.CharField(max_length =45)
    user_of_item = models.ManyToManyField(User, default=0, related_name = 'item_of_user')
    creator = models.ForeignKey(User, related_name="item_of_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()
