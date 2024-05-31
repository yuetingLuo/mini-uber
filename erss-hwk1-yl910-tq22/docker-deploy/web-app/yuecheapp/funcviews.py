import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.mail import EmailMessage
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from django.db.models import Model
from django.core.exceptions import MultipleObjectsReturned
import threading
from .models import User, Ride, Vehicle

@login_required
def main(request):
    return render(request, 'yuecheapp/main.html')

@login_required
@transaction.atomic
def ride_launch(request):
    if request.method == 'POST':
        try: 
            arrival_time = datetime.strptime(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'], 
                                        '%Y-%m-%d %H:%M')
            print(arrival_time)
            new_ride = Ride(dest_addr=request.POST['dest_addr'], 
                            arrival_time=arrival_time, 
                            passenger_num={},
                            passenger_cnt=int(request.POST['passenger_num']),
                            vehicle_type=request.POST['vehicle_type'], 
                            sp_info=request.POST['sp_info'], 
                            owner_id=request.user)
            new_ride.passenger_num[request.user.id] = request.POST['passenger_num']
            new_ride.is_shared = request.POST.get('is_shared', 'False') == 'True'
            new_ride.save()
        except Exception:
            return render(request, 'yuecheapp/ride_launch.html', {'error_message': 'Failed to launch ride! Please try again.'})
        return HttpResponseRedirect(reverse("yuecheapp:main"))
    else:
        return render(request, 'yuecheapp/ride_launch.html', {'current_user': request.user})

@login_required
def ride_search_driver(request):
    if request.user.vehicle_id is None:
        return render(request, 'yuecheapp/main.html', {'error_message': 'Please register as driver first!'})
    current_capacity = Vehicle.objects.get(driver_id=request.user.id).capacity
    current_vehicle_type = Vehicle.objects.get(driver_id=request.user.id).vehicle_type
    user_id_str = str(request.user.id)
    ride_set = Ride.objects.filter(Q(vehicle_type="") | Q(vehicle_type=current_vehicle_type),
                                   passenger_cnt__lte=current_capacity, 
                                   is_confirmed=False).exclude(Q(owner_id=request.user) | Q(passenger_num__has_key=user_id_str))
    return render(request, 'yuecheapp/ride_list.html', {'ride_set': ride_set, 'type': 'driver_search'})

@login_required
def ride_search_sharer(request):
    if request.method == 'POST':
        try:
            join_num = request.POST['passenger_num']
            from_time = datetime.strptime(request.POST['from_date'] + ' ' + request.POST['from_time'], 
                                        '%Y-%m-%d %H:%M')
            to_time = datetime.strptime(request.POST['to_date'] + ' ' + request.POST['to_time'], 
                                        '%Y-%m-%d %H:%M')
            user_id_str = str(request.user.id) 
            ride_set = Ride.objects.filter(
                                        dest_addr=request.POST['dest_addr'], 
                                        arrival_time__gte=from_time, 
                                        arrival_time__lte=to_time,
                                        is_shared=True,
                                        is_confirmed=False).exclude(Q(owner_id=request.user) | Q(passenger_num__has_key=user_id_str))
        except Exception:
            return render(request, 'yuecheapp/ride_search.html', {'error_message': 'Failed to do the search! Please try again.'})
        return render(request, 'yuecheapp/ride_search.html', {'ride_set': ride_set, 'join_num': join_num})
    else:
        return render(request, 'yuecheapp/ride_search.html')

@login_required
def ride_list_user(request):
    try:
        current_user_id = request.user.id
        current_date = timezone.now()
        print(current_date)
        ride_set = Ride.objects.filter(passenger_num__has_key=str(current_user_id), is_complete=False)
    except Exception:
        return render(request, 'yuecheapp/main.html', {'error_message': 'Failed to fetch the ride list! Please try again.'})
    return render(request, 'yuecheapp/ride_list.html', {'ride_set': ride_set, 'type': 'user_list', 'current_user': request.user,'current_date':current_date})


@login_required
def ride_list_driver(request):
    try:
        ride_set = Ride.objects.filter(driver_id=request.user.id, is_complete=False)
    except Exception:
        return render(request, 'yuecheapp/main.html', {'error_message': 'Failed to fetch the ride list! Please try again.'})
    return render(request, 'yuecheapp/ride_list.html', {'ride_set': ride_set, 'type': 'driver_list', 'current_user': request.user})

def safe_get_ride(request, ride_id):
    error_msg = ''
    ride = None
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        error_msg = 'This ride does not exist! Return in 3 seconds...'
    except MultipleObjectsReturned:
        error_msg = 'Multiple rides with the same ID, please check the validity of your database! Return in 3 seconds...'
    except Exception:
        error_msg = 'Failed to fetch the ride! Return in 3 seconds...'
    return (error_msg, ride)

@login_required
def ride_detail(request, ride_id):
    error_msg, ride = safe_get_ride(request, ride_id)
    if error_msg != '':
        return render(request, 'yuecheapp/main.html', {'error_message': error_msg})
    try :
        type = request.POST['type']
        if (type == 'driver_list' and type == 'driver_list' and request.user.id == ride.driver_id.id):
            pass
        elif type == 'user_list' and str(request.user.id) in ride.passenger_num:
            pass
        elif type == 'driver_search' or type == 'sharer_search':
            pass
        else:
            return render(request, 'yuecheapp/ride_detail.html', {'error_message': 'You are not allowed to view this ride! Return in 3 seconds...'})
        if ride.is_complete:
            return render(request, 'yuecheapp/ride_detail.html', {'error_message': 'This ride is already completed! Return in 3 seconds...'})
        join_num = -1
        if type == 'sharer_search':
            join_num = request.POST['join_num']
    except KeyError:
        return render(request, 'yuecheapp/ride_detail.html', {'error_message': 'You are trying to gain illegal access the data! Return in 3 seconds...'})
    return render(request, 'yuecheapp/ride_detail.html', {'ride': ride, 'current_user': request.user, 'type': type, 'join_num': join_num})

@login_required
@transaction.atomic
def ride_quit(request, ride_id):
    error_msg, ride = safe_get_ride(request, ride_id)
    if error_msg == "" and ride.is_confirmed:
        error_msg = 'You information are not up-to-date! Please check again. Return in 3 seconds...'
    if error_msg != '':
        return render(request, 'yuecheapp/main.html', {'error_message': error_msg})
    if str(request.user.id) not in ride.passenger_num:
        return render(request, 'yuecheapp/ride_detail.html', {'error_message': 'You are not allowed to view this ride! Return in 3 seconds...'})
    try:
        if request.user.id == ride.owner_id.id:
            ride.delete()
        else:
            ride.passenger_cnt -= int(ride.passenger_num[str(request.user.id)])
            ride.passenger_num.pop(str(request.user.id))
            ride.save()
    except Exception:
        return render(request, 'yuecheapp/ride_detail.html', {'op_error_msg': 'Failed to quit the ride! Please try again or refresh.'})
    return HttpResponseRedirect(reverse("yuecheapp:ride_list_user"))

@login_required
@transaction.atomic
def ride_modify(request, ride_id):
    error_msg, ride = safe_get_ride(request, ride_id)
    if error_msg == "" and ride.is_confirmed:
        error_msg = 'You information are not up-to-date! Please check again. Return in 3 seconds...'
    if error_msg != '':
        return render(request, 'yuecheapp/main.html', {'error_message': error_msg})
    if request.method == 'POST':
        try:
            if ride.owner_id.id == request.user.id:
                arrival_time = datetime.strptime(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'], 
                                                '%Y-%m-%d %H:%M')
                ride.dest_addr = request.POST['dest_addr']
                ride.arrival_time = arrival_time
                ride.passenger_cnt += int(request.POST['passenger_num']) - int(ride.passenger_num[str(request.user.id)])
                ride.passenger_num[str(request.user.id)] = request.POST['passenger_num']
                ride.vehicle_type = request.POST['vehicle_type']
                ride.sp_info = request.POST['sp_info']
                ride.is_shared = request.POST.get('is_shared', 'False') == 'True'
            else:
                ride.passenger_cnt += int(request.POST['passenger_num']) - int(ride.passenger_num[str(request.user.id)])
                ride.passenger_num[str(request.user.id)] = request.POST['passenger_num']
            ride.save()
        except Exception:
            return render(request, 'yuecheapp/ride_modify.html', {'error_message': 'Failed to modify the ride! Please try again.'})
        return HttpResponseRedirect(reverse("yuecheapp:ride_list_user"))
    else:
        arrival_date = ride.arrival_time.strftime('%Y-%m-%d')
        arrival_time = ride.arrival_time.strftime('%H:%M')
        passenger_num = ride.passenger_num[str(request.user.id)]
        return render(request, 'yuecheapp/ride_modify.html', {'ride': ride,
                                                            'current_user': request.user, 
                                                            'dest_addr': ride.dest_addr,
                                                            'arrival_date': arrival_date,
                                                            'arrival_time': arrival_time,
                                                            'passenger_num': passenger_num,
                                                            'vehicle_type': ride.vehicle_type,
                                                            'sp_info': ride.sp_info,
                                                            'is_shared': ride.is_shared})

@login_required
@transaction.atomic
def ride_join(request, ride_id):
    error_msg, ride = safe_get_ride(request, ride_id)
    if error_msg == "" and ride.is_confirmed:
        error_msg = 'You information are not up-to-date! Please check again. Return in 3 seconds...'
    if error_msg != '':
        return render(request, 'yuecheapp/main.html', {'error_message': error_msg})
    try:
        ride.passenger_num[str(request.user.id)] = request.POST['passenger_num']
        ride.passenger_cnt += int(request.POST['passenger_num'])
        ride.save()
    except Exception:
        return render(request, 'yuecheapp/ride_detail.html', {'op_error_msg': 'Failed to join the ride! Please try again or refresh.'})
    return HttpResponseRedirect(reverse("yuecheapp:main"))

def send_confirm_email(user, ride):
    template_path = os.path.join(settings.STATICFILES_DIRS[0], 'email', 'confirm_email.html')
    with open(template_path, 'r') as f:
        email_template = f.read()
    email_content = email_template.format(username=user.username, drivername=ride.driver_id.username, dest_addr=ride.dest_addr, 
                          arrival_time=ride.arrival_time, passenger_cnt=ride.passenger_cnt, 
                          vehicle_type=ride.driver_id.vehicle_id.vehicle_type, license_id=ride.driver_id.vehicle_id.license_id,
                          capacity=ride.driver_id.vehicle_id.capacity, sp_info=ride.driver_id.vehicle_id.sp_info)
    email = EmailMessage(
        'Your ride is confirmed!',
        email_content,
        settings.EMAIL_HOST,
        [user.email],
    )
    email.content_subtype = "html"
    try:
        email.send()
    except Exception:
        try:
            email.send()
        except Exception:
            email.send()

@login_required
@transaction.atomic
def ride_confirm(request, ride_id):
    error_msg, ride = safe_get_ride(request, ride_id)
    if error_msg == "" and (ride.is_confirmed or ride.passenger_cnt > request.user.vehicle_id.capacity or (ride.vehicle_type != "" and ride.vehicle_type != request.user.vehicle_id.vehicle_type)):
        error_msg = 'You information are not up-to-date! Please check again. Return in 3 seconds...'
    if error_msg != '':
        return render(request, 'yuecheapp/main.html', {'error_message': error_msg})
    ride.driver_id = request.user
    ride.is_confirmed = True
    try:
        ride.save()
    except Exception:
        return render(request, 'yuecheapp/ride_detail.html', {'op_error_msg': 'Failed to confirm the ride! Please try again or refresh.'})
    for user_id in ride.passenger_num:
        user = User.objects.get(id=int(user_id))
        email_thread = threading.Thread(target=send_confirm_email, args=(user, ride))
        email_thread.start()

    return HttpResponseRedirect(reverse("yuecheapp:ride_search_driver"))

@login_required
@transaction.atomic
def ride_complete(request, ride_id):
    error_msg, ride = safe_get_ride(request, ride_id)
    if error_msg == "" and ride.is_complete:
        error_msg = 'You information are not up-to-date! Please check again. Return in 3 seconds...'
    if error_msg != '':
        return render(request, 'yuecheapp/main.html', {'error_message': error_msg})
    ride.is_complete = True
    try:
        ride.save()
    except Exception:
        return render(request, 'yuecheapp/ride_detail.html', {'op_error_msg': 'Failed to complete the ride! Please try again or refresh.'})
    return HttpResponseRedirect(reverse("yuecheapp:ride_list_driver"))
