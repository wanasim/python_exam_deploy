from django.conf.urls import url
from . import views

app_name = 'wishList'

urlpatterns = [
    url(r'^add/(?P<id>\d+)$', views.addToList, name='add'),
    url(r'^remove/(?P<id>\d+)$', views.removeItem, name='remove'),
    url(r'^wish_items/(?P<id>\d+)$', views.itemInfo, name="itemInfo"),
    url(r'^deleteItem/(?P<id>\d+)$', views.deleteItem, name="delete"),
    url(r'^wish_items/add$', views.addItem, name='addItem'),
    url(r'^wish_items/create$', views.createItem, name='createItem'),
    url(r'^$', views.dashboard, name='dashboard'),
]
