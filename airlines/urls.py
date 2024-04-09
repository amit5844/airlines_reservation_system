from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login"),
    url(r'^report/$', views.airlineslisting, name="airlineslisting"),
    url(r'^book/$', views.bookticket, name="bookticket"),
    url(r'^search$', views.search, name="search"),
    url(r'^logout$', views.logout, name="logout"),
]
