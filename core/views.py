from .models import *
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
# from core.helpers.graph_functions import *
# from core.helpers.archive import *


class Home(TemplateView):
    template_name = "core/home.html"
    model = Farm

    def get_context_data(self, **kwargs):
 
        context = super(Home, self).get_context_data(**kwargs)
        # context['sensors'] = Sensor.objects.all()
        return context


class Test(TemplateView):
    template_name = "core/test_page.html"
    model = Farm

    def get_context_data(self, **kwargs):
 
        context = super(Test, self).get_context_data(**kwargs)
        # context['sensors'] = Sensor.objects.all()
        return context


class Main(LoginRequiredMixin, TemplateView):
    template_name = "core/main.html"
    model = Farm

    def get_context_data(self, **kwargs):
        logged_in_user = self.request.user
        # farm = Farm.objects.get(id=1)  # Replace with the ID of the farm you want to add the user to
        # farm.farmers.add(logged_in_user)
        context = super().get_context_data(**kwargs)
        try:
            # users_farms = Farm.objects.filter(farmers.user_id==logged_in_user.id)
            users_farms = logged_in_user.farms.all()
            # print(logged_in_user)  # print the logged-in user instance
            # print(logged_in_user.id)  # print the logged-in user instance
            # print(Farm.objects.filter(farmers=logged_in_user).query)  # print the generated SQL query
            # users_farms = Farm.objects.filter(farmers__in=[logged_in_user])
            # ic (len(users_farms))
            context['farms'] = users_farms
            context['chains'] = Chain.objects.all()
        except Farm.DoesNotExist:
            # Handle the case where the user doesn't have an associated farm
            context['farm'] = None  # Or some other appropriate value
            ic("No farm found for this user.")
            ic(logged_in_user)
        # else:
            # ic ("Trying to print the farm list")
            # ic (len(users_farms))
            # ic (logged_in_user)
            # for farm in users_farms:
            #     ic(farm.name)
            # farm = Farm.objects.get(id=1)  # Replace with the ID of the farm you want to check
            # if logged_in_user in farm.farmers.all():
            #     print("User is in the farmers field")
            # else:
            #     print("User is not in the farmers field")
        return context


class Utilities(TemplateView):
    template_name = "core/tabs.html"
    model = Chain

    def get_context_data(self, **kwargs):
 
        context = super(Utilities, self).get_context_data(**kwargs)
        context['granaries'] = Chain.objects.all()
        # context['sensors'] = Sensor.objects.all()
        return context
 

class ChainList(TemplateView):
    template_name = "core/chain_list.html"
    model = Farm

    def get_context_data(self, **kwargs):
        farm = Farm.objects.get(pk=self.kwargs["pk"])
        chains = Chain.objects.filter(farm=farm)
        context = super(ChainList, self).get_context_data(**kwargs)
        context['chains'] = chains
        # context['sensors'] = Sensor.objects.filter(chain=chains).order_by('depth')
        # context['num_of_readings'] = History.objects.filter(sensor__chain=granary).count()
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