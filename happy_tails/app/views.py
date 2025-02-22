from django.shortcuts import render,redirect,get_object_or_404
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
    if req.method == 'POST':
        id = req.POST['pet_id']
        name = req.POST['pet_name']
        gender = req.POST['pet_gender']
        age = req.POST['pet_age']
        adoption_fee = req.POST['adoption_fee']
        dis = req.POST['pet_description']
        file = req.FILES.get('pet_img')  # Ensure file upload works
        pet_category_id = req.POST['pet_category']
        try:
            pet_category = Pet_category.objects.get(id=pet_category_id)  # Ensure category exists
            data = Pets.objects.create(
                pet_id=id, 
                pet_name=name, 
                gender=gender, 
                age=age, 
                adoption_fee=adoption_fee, 
                dis=dis, 
                img=file, 
                category=pet_category
            )
            data.save()
            return redirect(shop_home)  # Redirect after successful submission
        except Pet_category.DoesNotExist:
            return render(req, 'shop/add_pet.html', {'error': 'Invalid category selected'})

    pets = Pet_category.objects.all()
    return render(req, 'shop/add_pet.html',{'pets':pets})


def edit_pet(req,id):
    pet=Pets.objects.get(pk=id)
    if req.method=='POST':
        e_id=req.POST['pet_id']
        name=req.POST['pet_name']
        gender=req.POST['pet_gender']
        age=req.POST['pet_age']
        adoption_fee=req.POST['adoption_fee']
        dis=req.POST['pet_description']
        file=req.FILES['pet_img']
        if file:
            Pets.objects.filter(pk=id).update(pet_id=e_id,pet_name=name,gender=gender,age=age,adoption_fee=adoption_fee,dis=dis,img=file)
        else:
            Pets.objects.filter(pk=id).update(pet_id=e_id,pet_name=name,gender=gender,age=age,adoption_fee=adoption_fee,dis=dis)
        return redirect(shop_home)
    return render(req,'shop/edit_pet.html',{'pets':pet})

# def delete_pet(req,id):
#     pet=Pet_category.objects.get(pk=id)
#     url=pet.image.url
#     url=url.split('/')[-1]
#     os.remove('media/'+url)
#     pet.delete()
#     return redirect(shop_home)



def dog_list(req,id):
    category = Pet_category.objects.get(id=id)
    pet_details = Pets.objects.filter(category=category)
    return render(req, 'shop/pet_list.html', {'category': category,'pet_details':pet_details})

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        send_mail('Happy Tails registration', 'Happy Tails account created', settings.EMAIL_HOST_USER, [email])
        try:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"Email Exists")
            return redirect(register)
    else:
        return render(req,'user/register.html')
    

def user_home(req):
    # if 'user' in req.session:
        pet=Pet_category.objects.all()
        return render(req,'user/user_home.html',{'pets':pet})
    # else:
        # return redirect(shop_login)

def view_pet(req,id):
    pet=Pets.objects.get(pk=id)
    return render(req,'user/view_pet.html',{'pets':pet})

