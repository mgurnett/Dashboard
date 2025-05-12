from django.db import models
from django.conf import settings
from datetime import datetime, date, timedelta
from icecream import ic
from django.db.models import F
from django.contrib.auth.models import User

'''
Design Philosophy:

All Model.properties return objects.
All formatting should be done in the templatetags layer.  
Helper functions should track which other functions are using them.
'''

class Farm(models.Model):
    ssid = models.CharField(max_length=100, blank = True)
    pw = models.CharField(max_length=100, blank = True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank = True)
    farmers = models.ManyToManyField(User, blank=True, related_name='farms')

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} at {self.location}"


class Chain(models.Model):
    ip = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank = True)
    name = models.CharField(max_length=100, unique=True)
    latest_update = models.DateTimeField(default=datetime(2000, 1, 1, 0, 0))
    serial_number = models.CharField(max_length=20)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
        
    @property
    def battery_voltage(self):
        battery = Status.objects.filter(chain=self).order_by('-recorded').first()
        return battery.battery
    
    @property
    def highest_current_temp(self):
        try:
            sensors = Sensor.objects.filter(chain=self)
            higest_readings = Reading.objects.filter(sensor__chain=self).order_by('-recorded').first()
        except:
            print("no sensors")
            return None
        else:
            # ic(higest_readings)
            return higest_readings
    
   
class Sensor(models.Model):
    wire1_id = models.CharField(max_length=100, unique=True)
    depth = models.IntegerField()
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    alarm = models.IntegerField(default = settings.DEFAULT_ALARM)

    class Meta:
        ordering = ["chain"]

    def __str__(self):
        return f"{self.chain.name} at {self.depth}ft"


class Reading(models.Model):
    ALARM_CHOICES = [(2, 'Cleared'), (1, 'In alarm'), (0, 'No alarm')]
    recorded = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    alarm_state = models.IntegerField(choices=ALARM_CHOICES, default=0)

    class Meta:
        ordering = ["recorded"]

    def __str__(self):
        return f"{self.sensor}"

    def __repr__(self):
        return f"{self.id} {self.recorded}:{self.sensor} > {self.value}"


class Archive(models.Model):
    ALARM_CHOICES = [(2, 'Cleared'), (1, 'In alarm'), (0, 'No alarm')]
    recorded = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    alarm_state = models.IntegerField(choices=ALARM_CHOICES, default=0)

    class Meta:
        ordering = ["recorded"]

    def __str__(self):
        return f"{self.sensor}"

    def __repr__(self):
        return f"{self.id} {self.recorded}:{self.sensor} > {self.value}"
    

class History(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    hour = models.DateTimeField()
    average = models.FloatField()
    high = models.FloatField()
    # high_time = models.DateTimeField()

    class Meta:
        ordering = ["hour"]

    def __str__(self):
        return f"{self.hour} {self.average} {self.high} {self.sensor}"

    def __repr__(self):
        return f"{self.id} {self.sensor} {self.hour} {self.average} {self.high}"
        

class Status (models.Model):
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    battery = models.FloatField()
    recorded = models.DateTimeField(default=datetime(2000, 1, 1, 0, 0))
    internal_temp = models.FloatField()
    error_log = models.CharField(max_length=200, blank = True)
    debug_log = models.CharField(max_length=200, blank = True)

    class Meta:
        ordering = ["chain"]

    def __str__(self):
        return f"{self.chain}"