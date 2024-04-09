from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection
from datetime import date


# Create your views here.

def printticket(request, id):
    context = {}
    context['passengars'] = getPassengers(id)
    context['booking_details'] = getBookingDetails(id)
    context['airlines_details'] = getAirlinesDetails(context['booking_details']['booking_route_id'])
    context['heading'] = "Book Details"
    return render(request, 'book-details.html', context)

def ticket(request):
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE `booking`
        SET booking_status=%s, booking_total=%s WHERE booking_id = %s		   
        """, (
        "Confirmed",
        request.POST['total_fare'],
        request.POST['booking_id']
        ))
        request.session['booking_id']= False
        request.session['route_id'] = False
    id = request.POST['booking_id']
    context = {}
    context['passengars'] = getPassengers(id)
    context['booking_details'] = getBookingDetails(id)
    context['airlines_details'] = getAirlinesDetails(context['booking_details']['booking_route_id'])

    # Message according Book #
    context['heading'] = "Book Details"
    return render(request, 'book-details.html', context)

def payment(request):
    cursor = connection.cursor()
    context = {
        "total_fare": request.POST['total_fare'],
        "booking_id": request.session['booking_id']
    }

    # Message according Book #
    context['heading'] = "Book Details";
    return render(request, 'book-payment.html', context)

def mybooking(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `users_user`,`booking` WHERE booking_user_id = user_id AND booking_status = 'Confirmed' AND booking_user_id = "+ str(request.session['user_id']))
    booklist = dictfetchall(cursor)

    context = {
        "booklist": booklist
    }

    # Message according Book #
    context['heading'] = "Book Details";
    return render(request, 'my-booking.html', context)

def getPassengers(bookingID):
    cursor = connection.cursor()
    print(bookingID)
    cursor.execute(
        "SELECT * FROM `booking`, `passengar` WHERE booking_id = passengar_booking_id AND booking_id = "+str(bookingID))
    return dictfetchall(cursor)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;


def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM book WHERE book_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];


def add(request):
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    if (request.method == "POST"):
        if(request.POST['act'] == "start_booking"):
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO `booking`
            SET booking_user_id=%s, booking_route_id=%s, booking_date=%s,  booking_journey_date=%s,  booking_status=%s		   
            """, (
                request.session['user_id'],
                request.POST['route_id'],
                d2,
                request.POST['date'],
                "Pending"))
            request.session['booking_id'] = cursor.lastrowid
            request.session['route_id'] = request.POST['route_id']
        elif(request.POST['act'] == "save_booking"):
            bookingID = request.session['booking_id']
            request.session['booking_id'] = 0
            return redirect('booking_details', id=bookingID)
        elif(request.POST['act'] == "save_passengar"):
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO passengar
            SET passengar_name=%s, passengar_gender=%s, passengar_age=%s, passengar_booking_id=%s		   
            """, (
                request.POST['passengar_name'],
                request.POST['passengar_gender'],
                request.POST['passengar_age'],
                request.session['booking_id']
                ))
            messages.add_message(request, messages.INFO, "Passengar added successfully !!!")

    context = {
        "fn": "add",
        "heading": 'Book Details',
        "route_id":request.session['route_id'],
        "airlines_details": getAirlinesDetails(request.session['route_id'])
    }
    if(request.session.get('booking_id')):
      context['passengars'] = getPassengers(request.session.get('booking_id'))
      context['booking_details'] = getBookingDetails(request.session['booking_id'])
      context['total_fare'] = getTotal(request.session['booking_id']) * int(context['airlines_details']['route_fare'])
      context['booking_id'] = request.session['booking_id']
    
    return render(request, 'book.html', context)


def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM passengar WHERE passengar_id=' + id
    cursor.execute(sql)
    return redirect('mybooking')

def getProductCost(productId):
    cursor = connection.cursor()
    cursor.execute("SELECT product_cost FROM product_product WHERE product_id = " + str(productId))
    dataList = dictfetchall(cursor)
    return dataList[0]['product_cost']

def getTotal(bookingID):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) as total_count FROM `passengar` WHERE passengar_booking_id = " + str(bookingID))
    dataList = dictfetchall(cursor)
    return dataList[0]['total_count']

def getBookingDetails(bookingID):
    if(bookingID):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `booking` WHERE booking_id = " + str(bookingID))
        dataList = dictfetchall(cursor)
        return dataList[0]


def getAirlinesDetails(routeID):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM airlines_city, company, route, airlines WHERE city_id = airlines_from AND airlines_id = route_airlines_id AND company_id = airlines_company_id AND route_id = "+routeID)
    dataList = dictfetchall(cursor)
    return dataList[0]

def delete_oi(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM passengar WHERE passengar_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Passengar deleted successfully !!!")
    return redirect('add')
