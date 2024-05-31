from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #Fields: username, password, email 
    # and method email_user() in AbstractUser class
    vehicle_id = models.OneToOneField('Vehicle', on_delete=models.SET_NULL, null=True)


class Ride(models.Model):
    dest_addr = models.CharField(max_length=255)
    arrival_time = models.DateTimeField()
    # {"user1": "passenger_num", "user2": "passenger_num"} 
    passenger_num = models.JSONField()
    passenger_cnt = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=255, default="")
    sp_info = models.TextField(null=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_owner')
    driver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_driver', null=True)
    is_shared = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Ride: {self.dest_addr} (ID: {self.owner_id})"


class Vehicle(models.Model):
    driver_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=255)
    license_id = models.IntegerField()
    capacity = models.IntegerField()
    sp_info = models.TextField()

    def __str__(self):
        return f"Vehicle: {self.vehicle_type} (ID: {self.license_id})"


