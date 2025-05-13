from django import template
from django.utils.safestring import mark_safe
from django.db import models
from datetime import datetime, date, timedelta
from django.utils import timezone
from icecream import ic
import pytz

register = template.Library()


@register.simple_tag
def date_format(latest_update_naive):
    edmonton_tz = pytz.timezone('America/Edmonton')

    # Make the naive latest_update timezone-aware as Edmonton time
    # latest_update_edmonton = edmonton_tz.localize(latest_update_naive)
    latest_update_edmonton = latest_update_naive

    # Get the current time in Edmonton
    now_edmonton = timezone.localtime(timezone.now(), timezone=edmonton_tz)

    time_difference = now_edmonton - latest_update_edmonton
    print (f"local time (Edmonton): {now_edmonton} and latest update (Edmonton): {latest_update_edmonton} and time difference: {time_difference}")
    if time_difference > timedelta(hours=1):
        return mark_safe(f'<div class="text-danger">{latest_update_edmonton.strftime("%a, %b %d @ %-I:%M:%S %p")}</div>')
    else:
        return mark_safe(f'<div class="text-success">{latest_update_edmonton.strftime("%a, %b %d @ %-I:%M:%S %p")}</div>')
    
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