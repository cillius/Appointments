from django.conf.urls import url
from .import views

urlpatterns=[
  url(r'^$',views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^home$', views.home),
  url(r'^logout$', views.logout),
  url(r'^home$', views.home),
  url(r'^delete/(?P<id>\d+)',views.delete),
  url(r'^(?P<id>\d+)',views.edit),
  url(r'^update/$',views.update),
  url(r'^update/(?P<id>\d+)',views.update),
  url(r'^create$',views.create)
]
