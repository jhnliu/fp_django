
# Load required package from django
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic

from rest_framework.parsers import JSONParser
from rest_framework import status

import os
import json
import heapq
import pymongo
import traceback
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from .models import Food
from .forms import FoodForm
from .serializers import FoodSerializer
from rest_framework.decorators import api_view

# Load tensorflow model
try:
    model = tf.keras.models.load_model('fp/src/13Oct_62food')
    print("Successfully loaded model.")
except:
    print("Could not load tensorflow model.")

# Load database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["fp_mongo"]
food_data = db['fp_food']

# Connect to food data
with open('fp/src/food_data.json', 'r') as f:   # Change to food and name matching
    data = json.load(f)

# Get request for checking the available food
@login_required()
def f_data(request):
    return HttpResponse(data)

#Can we construct the picking tips, variety and origin immediately after the image classification
# # Get request for variety
# def get_variety(request):
#     return render(request, 'homepage.html')

# # Get request for for origin
# def get_origin(request):
#     return render(request, 'homepage.html')

# POST request for Image Classification to return the food object
def predict(request):
    if  request.method == "POST":
        f=request.FILES['sentFile']
        file_name = "unnamed.jpg"
        file_name_2 = default_storage.save(file_name, f) #
        file_url = default_storage.url(file_name_2)

        # load and preprocess the image
        img = plt.imread('/Users/foodpicker/fp/fp_django/'+file_url)

        img = tf.image.resize_with_crop_or_pad(img, 200,200) # To be changed to 224 when new model is ready
       
        # Get the predictions and return the top 5
        img = tf.stack([img], axis=0)
        pred = model.predict(img)
        top_5 = heapq.nlargest(5, range(len(pred[0])), key=pred[0].__getitem__)

        food = []
        for i in top_5:
            food.append(food_data.find_one({'ID': i}))
        
        response = {}
        response['food_predictions'] = str(food)
        response['photo_name'] = file_name_2
        # return JsonResponse(food, safe=False)
        return render(request,'homepage.html',response)

    else:
        print("Something is wrong.")
        return render(request,'homepage.html')

# Assumption: User click on the button and send a request with the food label
def name_photo(request):

    if request.method == 'POST':
        storage = '/Users/foodpicker/fp/fp_django/fp/media/'

        old_name = storage + request.POST.get('old_name') + '.jpg'
        new_name = storage + request.POST.get('new_name') + '.jpg'

        os.rename(old_name, new_name)
        print("Photo renamed from {} to {}".format(old_name, new_name))

        # Move the photo to the corresponding file
        response = {}
        return render(request,'choose_food.html',response)


    else:
        print('Rename is not working....try again.')
        return render(request, 'choose_food.html')
    

# Login page
def user_login(request):
    return HttpResponse("This is the login page.")

# User registration page
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    redirect_field_name = 'fp:login'


@api_view(['GET', 'POST', 'DELETE'])
def food_list(request):

    # Retrieve an object with condition
    if request.method == 'GET':
        foods = Food.objects.all()
        
        engName = request.GET.get('engName', None)
        if engName is not None:
            foods = foods.filter(title__icontains=engName)
        
        food_serializer = FoodSerializer(foods, many=True)
        return JsonResponse(food_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    # Creat a new object
    elif request.method == 'POST':
            food_data = JSONParser().parse(request)
            food_serializer = FoodSerializer(data=food_data)
            if food_serializer.is_valid():
                food_serializer.save()
                return JsonResponse(food_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(food_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def food_details(request, food_id):

    # find food by food_id (id)
    try:
        food = Food.objects.get(food_id=food_id)
    except food.DoesNotExist: 
        return JsonResponse({'message': 'The food does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    # Retrieve the object
    if request.method == 'GET': 
        food_serializer = FoodSerializer(food) 
        return JsonResponse(food_serializer.data) 

    # Update the object
    elif request.method == 'PUT': 
        food_data = JSONParser().parse(request) 
        food_serializer = FoodSerializer(food, data=food_data) 
        if food_serializer.is_valid(): 
            food_serializer.save() 
            return JsonResponse(food_serializer.data) 
        return JsonResponse(food_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    # Delete an object according to the pk
    elif request.method == 'DELETE': 
        Food.delete() 
        return JsonResponse({'message': 'food was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def food_list_published(request):
    # GET all published foods
    foods = Food.objects.filter(published=True)
        
    if request.method == 'GET': 
        foods_serializer = FoodSerializer(foods, many=True)
        return JsonResponse(foods_serializer.data, safe=False)
