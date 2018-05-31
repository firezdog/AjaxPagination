from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^ajax-index$', views.ajaxIndex),
    url(r'^create$', views.create, name="my_create"),
    url(r'^(?P<id>\d+)/destroy$', views.destroy, name='my_destroy'),
    url(r'^update$', views.update)
]