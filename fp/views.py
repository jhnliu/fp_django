from django.shortcuts import render, get_object_or_404

# Load required package from django
from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
# from django.template import loader
# from .models import Question, Choice

import json
import tensorflow as tf

with open('fp/src/food_data.json', 'r') as f:
    food = json.load(f)

def food_data(request):
    return HttpResponse(food)

def predict(request):
    
    pass
