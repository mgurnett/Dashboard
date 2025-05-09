from .models import *
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import View
# from core.helpers.graph_functions import *
# from core.helpers.archive import *


class Home(TemplateView):
    template_name = "core/home.html"
    model = Farm

    def get_context_data(self, **kwargs):
 
        context = super(Home, self).get_context_data(**kwargs)
        context['farm'] = Farm.objects.all()
        # context['sensors'] = Sensor.objects.all()
        return context


class Utilities(TemplateView):
    template_name = "core/tabs.html"
    model = Chain

    def get_context_data(self, **kwargs):
 
        context = super(Utilities, self).get_context_data(**kwargs)
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