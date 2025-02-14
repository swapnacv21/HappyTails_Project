from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['shop']=uname    #--------------->creating session
                return redirect(shop_home)
            else:
                login(req,data)
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,"Invalid username or password")
            return redirect(shop_login)
    else:
        return render(req,'login.html')
    


def shop_logout(req):
    logout(req)
    req.session.flush()      #-------------------delete session
    return redirect(shop_login)
    

def shop_home(req):
    if 'shop' in req.session:
        pet=Pet_category.objects.all()
        return render(req,'shop/home.html',{'pets':pet})
    else:
        return redirect(shop_login)
    

def add_pet(req):
    if req.method=='POST':
        id=req.POST['pet_id']
        name=req.POST['pet_name']
        gender=req.POST['pet_gender']
        age=req.POST['pet_age']
        adoption_fee=req.POST['adoption_fee']
        dis=req.POST['pet_description']
        file=req.FILES['pet_img']
        pet_category=req.POST['pet_category']
        data=Pets.objects.create(pet_id=id,pet_name=name,gender=gender,age=age,adoption_fee=adoption_fee,dis=dis,img=file,category=pet_category)
        data.save()
        return redirect(shop_home)
    return render(req,'shop/add_pet.html')


def dog_list(req,id):
    category = Pet_category.objects.get(id=id)
    pet_details = Pets.objects.filter(category=category)
    return render(req, 'shop/pet_list.html', {'category': category,'pet_details':pet_details})

