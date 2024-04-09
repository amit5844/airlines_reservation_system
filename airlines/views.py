from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import airlines, city, state, country, airlines, type
from django.contrib import messages
from django.db import connection


# Create your views here.

def airlineslisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM airlines_airlines, airlines_type WHERE type_id = airlines_type_id")
    airlineslist = dictfetchall(cursor)

    context = {
        "airlineslist": airlineslist
    }
    context['heading'] = "Airlines Records";
    return render(request, 'airlines-listing.html', context)

def bookticket(request):
    cursor = connection.cursor()
    # cursor.execute(
    #     "SELECT * FROM airlines, airlines_type WHERE type_id = airlines_type_id")
    # airlineslist = dictfetchall(cursor)
    airlineslist = ""
    context = {
        "airlineslist": airlineslist
    }
    context['heading'] = "Airlines Records";
    return render(request, 'airlines-details.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def search(request):
    context = {
    "fn":"add",
    "citylist":city.objects.all(),
    "heading":'Airlines Management',
    "sub_heading": 'Airliness',
    }
    if (request.method == "POST"):
        try:
           cursor = connection.cursor()
           cursor.execute("SELECT * FROM airlines_city, company, route, airlines WHERE city_id = airlines_from AND airlines_id = route_airlines_id AND company_id = airlines_company_id AND route_from_city = "+request.POST['from_city']+" AND route_to_city = "+request.POST['to_city'])
           airlineslist = dictfetchall(cursor)
           context = {
                "airlineslist": airlineslist,
                "date": request.POST['travel_date']
            }
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return render(request,'listing.html', context)

    else:
        return render(request,'airlines-search.html', context)

def logout(request):
    request.session['authenticated']= False
    request.session['user_id'] = False
    request.session['user_level_id'] = False
    request.session['user_name']= False
    return redirect('/')

# Create your views here.
def index(request):
    if(request.session.get('authenticated', False) == True):
        return redirect('/users/dashboard')

    context = {
        "message": "Please Log in",
        "error": False
    }
    if(request.method == "POST"):
        try:
            getUser = airlines.objects.get(airlines_number=request.POST['username'])
            context['msg'] = getUser
        except:
            context['message'] = "Wrong username"
            context['error'] = True
            return render(request,'airlines-login.html', context)
        if(getUser.airlines_travel_station == request.POST['password']):
            request.session['authenticated'] = True
            request.session['user_id'] = getUser.airlines_id
            request.session['user_level_id'] = 2
            request.session['user_name'] = getUser.airlines_name
            return redirect('/users/dashboard')
        else:
            context['message'] = "Wrong Password"
            context['error'] = True
            return render(request,'airlines-login.html', context)
    else:
        return render(request,'airlines-login.html', context)