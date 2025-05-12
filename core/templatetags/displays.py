from django import template
from django.utils.safestring import mark_safe
from django.db import models
from datetime import datetime, date, timedelta
from icecream import ic

register = template.Library()


@register.simple_tag
def date_format(latest_update):
    if latest_update == datetime(2000, 1, 1, 0, 0):
        return ""   
    else:
        now = datetime.now()  # Use timezone.now()
        time_difference = now - latest_update
        if time_difference > timedelta(hours=1):
            return mark_safe(f'<div class="text-danger">{latest_update.strftime("%a, %b %d @ %-I:%M:%S %p")}</div>')
        else:
            return mark_safe(f'<div class="text-success">{latest_update.strftime("%a, %b %d @ %-I:%M:%S %p")}</div>')
    
@register.simple_tag
def battery_voltage__html(voltage):
    if voltage == None:
        return ""
    if voltage > 3.6:
        return mark_safe(f'<div class="text-success">{round(voltage, 1)}V</div>')
    elif voltage < 3.6 and voltage > 3.1:
        return mark_safe(f'<div class="text-warning">{round(voltage, 1)}V</div>')
    else: 
        return mark_safe(f'<div class="text-danger">{round(voltage, 1)}V</div>')


@register.simple_tag
def temp_text_colour__html(value, alarm, alarm_state): #float, int, object
    if value:
        # ic (value, alarm, alarm_state)
        temp = round(value, 1)

        if alarm_state == 2:
            colour = "info"
        else:
            if value > alarm:
                colour = "danger"
            elif (value + 5) > alarm:
                colour = "warning"
            elif (value + 10) > alarm:
                colour = "warning"
            elif (value + 15) > alarm:
                colour = "secondary"
            else:
                colour = ""

        return mark_safe(f'<div class="text-{colour}">{temp}°C</div>')
    else:
        return  ""