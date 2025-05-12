from django import template
from django.utils.safestring import mark_safe
from django.db import models
from datetime import datetime, date, timedelta
from icecream import ic

register = template.Library()

@register.simple_tag
def temp_with_colour__html(value, alarm, alarm_state): #float, int, object
        # ic (value, alarm, alarm_state)
        temp = round(value, 1)
        temp_value__str = f"{temp}°C"

        if alarm_state == 2:
            colour = "purple"
        else:
            if value > alarm:
                colour = "red"
            elif (value + 5) > alarm:
                colour = "orange"
            elif (value + 10) > alarm:
                colour = "yellow"
            elif (value + 15) > alarm:
                colour = "khaki"
            else:
                colour = ""

        return mark_safe(f'<button class="w3-button w3-{colour}">{temp_value__str}</button>')

@register.simple_tag
def temp_text_colour__html(value, alarm, alarm_state): #float, int, object
        # ic (value, alarm, alarm_state)
        temp = round(value, 1)

        if alarm_state == 2:
            colour = "purple"
        else:
            if value > alarm:
                colour = "red"
            elif (value + 5) > alarm:
                colour = "orange"
            elif (value + 10) > alarm:
                colour = "yellow"
            elif (value + 15) > alarm:
                colour = "khaki"
            else:
                colour = ""

        return mark_safe(f'<span class="w3-text-{colour}">{temp}°C</span>')
        
@register.simple_tag
def date_format(latest_update):
    if latest_update == datetime(2000, 1, 1, 0, 0):
        return ""   
    else:
        now = datetime.now()  # Use timezone.now()
        time_difference = now - latest_update
        if time_difference > timedelta(hours=1):
            return mark_safe(f'<div class="w3-text-red">{latest_update.strftime("%a, %b %d @ %-I:%M:%S %p")}</div>')
        else:
            return mark_safe(f'<div class="w3-text-green">{latest_update.strftime("%a, %b %d @ %-I:%M:%S %p")}</div>')
    
@register.simple_tag
def alarm_state__html(state):
    if state == 0:
        return mark_safe('<button class="w3-button w3-green">No alarm</button>')
    elif state == 1:
        return mark_safe('<button class="w3-button w3-red">ALARM</button>')
    else: 
        return mark_safe('<button class="w3-button w3-purple">Alarm cleared</button>')
    
@register.simple_tag
def battery_voltage__html(voltage):
    if voltage == None:
        return ""
    if voltage > 3.6:
        return mark_safe(f'<span class="w3-text-green">{round(voltage, 1)}V</span>')
    elif voltage < 3.6 and voltage > 3.1:
        return mark_safe(f'<span class="w3-text-orange">{round(voltage, 1)}V</span>')
    else: 
        return mark_safe(f'<span class="w3-text-red">{round(voltage, 1)}V</span>')