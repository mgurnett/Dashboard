from django.db import models
from django.conf import settings
from datetime import datetime, date, timedelta
from icecream import ic
from django.db.models import F

'''
Design Philosophy:

All Model.properties return objects.
All formatting should be done in the templatetags layer.  
Helper functions should track which other functions are using them.
'''

class Chain(models.Model):
    ''' The Chain model represents a granary or a collection of sensors.

    Fields
        description: A character field to store a brief description of the chain. (max_length=100, blank=True)
        name: A character field to store the name of the chain. (max_length=100, unique=True)
        ip: A character field to store the IP address of the chain. (max_length=20, unique=True)
        last_update: A date field to store the last time the chain was updated. (default=datetime(2000, 1, 1, 0, 0)) used for API adds.
    Properties
        num_of_sensors: Returns the number of sensors associated with this chain.
        num_of_readings: Returns the number of readings associated with this chain.
        highest_current_temp: Returns the highest current temperature reading for this chain.
    Methods
        __str__: Returns a string representation of the chain, which is the chain's name.
    '''
    ip = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank = True)
    name = models.CharField(max_length=100, unique=True)
    latest_update = models.DateTimeField(default=datetime(2000, 1, 1, 0, 0))
    serial_number = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
    @property
    def num_of_sensors(self):
        return Sensor.objects.filter(chain=self).count()
    
    @property
    def num_of_readings(self):
        return Reading.objects.filter(sensor__chain=self).count()

    @property
    def data_for_graph(self):
        return Reading.objects.filter(sensor__chain=self).annotate(sensor_depth=F('sensor__depth')).order_by('recorded').values('recorded', 'sensor_depth','value')
    
    @property
    def data_for_history_graph(self):
        return History.objects.filter(sensor__chain=self).annotate(sensor_depth=F('sensor__depth')).order_by('hour').values('hour', 'sensor_depth','average', 'high')

    @property
    def data_for_battery_graph(self):
        return Status.objects.filter(chain=self).order_by('recorded').values('recorded', 'battery', 'internal_temp')
    
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
        
    @property
    def battery_voltage(self):
        battery = Status.objects.filter(chain=self).order_by('-recorded').first()
        return battery.battery
        
    @property
    def internal_temperature(self):
        temperature = Status.objects.filter(chain=self).order_by('-recorded').first()
        return f"{round(temperature.internal_temp, 1)}°C"
    
   
class Sensor(models.Model):
    ''' The Sensor model represents a temperature sensor.

    Fields
        wire1_id: A character field to store the unique identifier of the sensor. (max_length=100, unique=True)
        depth: An integer field to store the depth of the sensor.
        chain: A foreign key field to associate the sensor with a chain.
        alarm: An integer field to store the alarm temperature for the sensor. (default=settings.DEFAULT_ALARM)
    Properties
        num_of_readings: Returns the number of readings associated with this sensor.
    Methods
        __str__: Returns a string representation of the sensor, which includes the chain's name and the sensor's depth.
    '''
    wire1_id = models.CharField(max_length=100, unique=True)
    depth = models.IntegerField()
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    alarm = models.IntegerField(default = settings.DEFAULT_ALARM)

    class Meta:
        ordering = ["chain"]

    def __str__(self):
        return f"{self.chain.name} at {self.depth}ft"
    
    @property
    def depth__str(self):
        return f"{self.depth}ft"
    
    @property
    def num_of_readings(self):
        return Reading.objects.filter(sensor=self).count()
    
    @property
    def high_reading(self): # this is used by the highest_current_temp def in Chain.
        try:
            return Reading.objects.filter(sensor=self).order_by('-recorded').first()
        except Reading.DoesNotExist:
            return None
    
    @property
    def latest_reading(self):  
        # this is used in two places.  
        # The first is the chain_detail page and 
        # the second is the chain.highest_current_temp_M
        try:
            reading = Reading.objects.filter(sensor=self).order_by('-recorded').first()
            return reading
        except:
            return None
    
    @property
    def alarm__str(self):
        return f"{self.alarm}°C"


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
    
    @property
    def value__str(self):
        return f"{round(self.value, 1)}°C"


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

    @property
    def data_for_graph(self):
        return History.objects.filter(sensor__chain=self).annotate(sensor_depth=F('sensor__depth')).order_by('hour').values('hour', 'sensor_depth','average', 'high')
    

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