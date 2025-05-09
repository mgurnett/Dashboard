from .models import *
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import View
from core.helpers.graph_functions import *
from core.helpers.archive import *


class Utilities(TemplateView):
    template_name = "core/tabs.html"
    model = Chain

    def get_context_data(self, **kwargs):
 
        context = super(Utilities, self).get_context_data(**kwargs)
        context['granaries'] = Chain.objects.all()
        # context['sensors'] = Sensor.objects.all()
        return context


class Home(TemplateView):
    template_name = "core/homeW3.html"
    model = Reading

    def get_context_data(self, **kwargs):
 
        context = super(Home, self).get_context_data(**kwargs)
        context['granaries'] = Chain.objects.all()
        # context['sensors'] = Sensor.objects.all()
        return context
 

class GranaryDetail(TemplateView):
    template_name = "core/granary_detail.html"
    model = Chain

    def get_context_data(self, **kwargs):
        granary = Chain.objects.get(pk=self.kwargs["pk"])
        context = super(GranaryDetail, self).get_context_data(**kwargs)
        context['granary'] = granary
        context['sensors'] = Sensor.objects.filter(chain=granary).order_by('depth')
        context['num_of_readings'] = History.objects.filter(sensor__chain=granary).count()
        return context
 

class GranaryVisual(TemplateView):
    template_name = "core/granary_visual.html"
    model = Chain

    def get_context_data(self, **kwargs):
        granary = Chain.objects.get(pk=self.kwargs["pk"])
        context = super(GranaryVisual, self).get_context_data(**kwargs)
        context['granary'] = granary
        context['sensors'] = Sensor.objects.filter(chain=granary).order_by('depth')
        context['num_of_readings'] = Reading.objects.filter(sensor__chain=granary).count()
        context['graph'] = granary_graph(granary).to_html()
        return context
    
class SensorDetail(TemplateView):
    template_name = "core/sensor_detail.html"
    model = Sensor

    def get_context_data(self, **kwargs):
        sensor = Sensor.objects.get(pk=self.kwargs["pk"])
        context = super(SensorDetail, self).get_context_data(**kwargs)
        context['sensor'] = sensor
        context['readings'] = Reading.objects.filter(sensor=sensor).order_by('-recorded')[:50]
        # context['num_of_readings'] = Reading.objects.filter(reading__sensor=sensor).count()
        return context
    

class GranaryGraph(TemplateView):        
    template_name = "core/granary_graph.html"
    model = Chain

    def get_context_data(self, **kwargs):
        granary = Chain.objects.get(pk=self.kwargs["pk"])
        context = super(GranaryGraph, self).get_context_data(**kwargs)
        context['granary'] = granary
        context['graph'] = granary_graph_history(granary).to_html() 
        return context
    

class Battery_graph(TemplateView):
    template_name = "core/battery_graph.html"
    model = Status

    def get_context_data(self, **kwargs):
        granary = Chain.objects.get(pk=self.kwargs["pk"])
        context = super(Battery_graph, self).get_context_data(**kwargs)
        context['granary'] = granary
        context['graph'] = granary_graph_battery(granary).to_html()
        return context
    

# ============LIVE UPDATES================= 


class GetGraphView(View):
    def get(self, request, pk):
        granary = get_object_or_404(Chain, pk=pk)
        graph = granary_graph(granary).to_html()
        return render(request, 'core/htmx/g_v/graph.html', {'graph': graph})
   

def get_temp(request, pk): # pk because it is the primary key
    sensor = get_object_or_404(Sensor, pk=pk)
    return render(request, 'core/htmx/g_v/temp.html', {'sen': sensor})  # Pass the sensor object


def live_latest_update(request, pk):
    bin = get_object_or_404(Chain, pk=pk)
    return render(request, 
                  'core/homeW3.html#latest_update',
                  {'granary': bin}
                  )


def live_high_temp_update(request, pk):
    bin = get_object_or_404(Chain, pk=pk)
    return render(request, 
                  'core/homeW3.html#highest_temp',
                  {'granary': bin}
                  )


def live_battery_update(request, pk):
    bin = get_object_or_404(Chain, pk=pk)
    return render(request, 
                  'core/homeW3.html#battery_voltage',
                  {'granary': bin}
                  )



# ============BUTTONS=================    

def Alarm_Clear(request, pk):
    bin = Chain.objects.get(pk=pk)
    readings = Reading.objects.filter(sensor__chain=bin, alarm_state=1)
    readings.update(alarm_state=2)
    return redirect('granary_visual', pk)
     

def Archive_data(request):
    archive()
    return redirect('core_home')

    
def Battery_replace(request, pk):
    bin = Chain.objects.get(pk=pk)
    delete = Status.objects.filter(chain=bin).delete()
    return redirect('granary_detail', pk)