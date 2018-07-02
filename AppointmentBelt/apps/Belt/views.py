#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User,Appointment
from datetime import datetime
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):            
    return render(request,'index.html')

def home(request):
    
    now=datetime.now().strftime("%Y-%m-%d"),
    user=User.objects.get(id=request.session['user_id'])
    today=Appointment.objects.order_by('date').filter(date=datetime.now(), key=user)
    laterdate=Appointment.objects.order_by('date').filter(key=user).exclude(date=datetime.now())
    print("Todays appointmentList: ", today)
    print("Latter appointmentList: ", laterdate)
    context={
    'user':user,
    'laterdate':laterdate,
    'today':today,
    'now':now
    }
    return render(request,"welcome.html",context)

def register(request):
    errors = User.objects.validate(request.POST)
    #print 'this process works', request.POST
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect("/")

    else:
        hashpwd = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        newuser = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashpwd)

        request.session['user_id'] = newuser.id
        request.session['name'] = newuser.first_name
        print "session info", newuser.id, newuser.first_name
        return redirect("/home")

def login(request):
    errors = User.objects.loginvalidate(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'])[0]
        request.session['user_id'] = user.id
        request.session['name'] = user.first_name
        return redirect("/home")

def logout(request):
    request.session.clear()
    print 'goodbye'
    return redirect('/')
def delete(request,id):
    Appointment.objects.get(id=id).delete()
    return redirect('/home')

def edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {'edit': Appointment.objects.get(id=id)}
    context['id'] = id
    print(context['id'])
    return render(request, "update.html", context)
def create(request):
    errors=Appointment.objects.appointvalidate(request.POST)
    if len(errors)>0:
        for error in errors:
            messages.error(request,error)
        return redirect("/home")
    else:
        users = User.objects.get(id = request.session['user_id'])
        Appointment.objects.create(
        task=request.POST["task"],
        clock=request.POST["clock"],
        date=request.POST["date"],
        status="Pending",
        key=users,
        )
        print("Date of appointmment", request.POST["date"])
        return redirect("/home")

def update(request,id=None):
    errors=Appointment.objects.appointvalidate(request.POST)
    if len(errors)>0:
        for error in errors:
            messages.error(request,error)
        return redirect("/{}".format(id))
    print(request.POST)
    #if errors['status']==True:
    up=Appointment.objects.get(id=id)
    up.task=request.POST['task']
    up.clock=request.POST['clock']
    up.date=request.POST['date']
    up.status=request.POST['status']
    up.save()
    return redirect("/home")
        
    #else:
    #    if len(errors)>0:
    #        for error in errors:
    #            messages.error(request,error)
    #    return redirect('/{}')
