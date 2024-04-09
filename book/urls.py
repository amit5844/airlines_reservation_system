from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mybooking, name="mybooking"),
    url(r'^add$', views.add, name="add"),
    url(r'^payment$', views.payment, name="payment"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^ticket$', views.ticket, name="ticket"),
    url(r'^print-ticket/(?P<id>\w{0,50})/$', views.printticket, name="printticket"),
    url(r'^delete/items/(?P<id>\w{0,50})/$', views.delete_oi, name="delete_oi"),
]

