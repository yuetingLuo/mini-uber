from django.shortcuts import render, redirect
from yuecheapp.models import User, Vehicle
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, logout as auth_logout,login as auth_login
from django.contrib.auth.decorators import login_required

def root(request):
    return redirect(reverse('yuecheapp:login'))

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect(reverse('yuecheapp:main'))
        else:
            return render(request, 'yuecheapp/login.html', {'error_message': 'Invalid credentials'})
    
    return render(request, "yuecheapp/login.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('yuecheapp:login'))

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Check if username is unique
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return render(request, 'yuecheapp/user_register.html', {'error_message': 'Username is already taken'})

            # create new user
            user = User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('yuecheapp:login'))
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'yuecheapp/user_register.html')
        
@login_required
def driver_register(request):
    if request.method == 'POST':
        try:
            vehicle_type = request.POST.get("vehicle_type")
            license_id = request.POST.get("license_id")
            capacity = request.POST.get("capacity")
            sp_info = request.POST.get("sp_info","")
            user = request.user

            # create new vehicle
            vehicle = Vehicle.objects.create(driver_id = user,vehicle_type=vehicle_type, license_id=license_id, capacity=capacity, sp_info=sp_info)
            vehicle.save()

            #refresh user field
            user.vehicle_id = vehicle
            user.save()

        except Exception:
            return render(request,'yuecheapp/driver_register.html', {'error_msg':'Input of License ID or Capacity should be integer.'})     
        
        return redirect(reverse('yuecheapp:profile'))
    
    return render(request, "yuecheapp/driver_register.html")

@login_required
def profile(request):
    user = request.user
    vehicle = user.vehicle_id
    return render(request, 'yuecheapp/profile.html', {'user': user, 'vehicle': vehicle})

@login_required
def profile_modify(request):
    user = request.user
    vehicle = user.vehicle_id

    if request.method == 'POST':
        user.email = request.POST.get('email')
        try:
            if vehicle is not None:
                vehicle.vehicle_type = request.POST.get('vehicle_type')
                vehicle.license_id = request.POST.get('license_id')
                vehicle.capacity = request.POST.get('capacity')
                vehicle.sp_info = request.POST.get('sp_info', '')
                vehicle.save()

            user.save()
        except Exception:
            return render(request,'yuecheapp/profile_modify.html', {'error_msg':'Input of License ID or Capacity should be integer.'})     
        
        return redirect(reverse('yuecheapp:profile')) 

    return render(request, 'yuecheapp/profile_modify.html', {'user': user, 'vehicle': vehicle})

