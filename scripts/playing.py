from core.models import *
from django.conf import settings
import icecream

def run():
    logged_in_user = User.objects.get(id=1)
    ic (logged_in_user)


    farm = Farm.objects.get(id=2)  # Replace with the ID of the farm you want to add the user to
    farm.farmers.add(logged_in_user)

    users_farms = Farm.objects.filter(farmers=logged_in_user)
    ic (len(users_farms))

