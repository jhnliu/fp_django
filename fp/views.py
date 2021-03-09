
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
from django.views.decorators.csrf import csrf_exempt
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
from datetime import datetime, timedelta
import numpy as np
from .models import Food
from .forms import FoodForm
from .serializers import FoodSerializer
from rest_framework.decorators import api_view

# Load tensorflow model
try:
    # Change the model when more food is availabel
    model = tf.keras.models.load_model('fp/src/13Oct_62food')
    print("Successfully loaded model.")
except:
    print("Could not load tensorflow model.")

# Load database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["fp_mongo"]
food_data = db['fp_food']
user_data = db['fp_user']
user_log = db['fp_user_log']

# Connect to food data
with open('fp/src/food_data.json', 'r') as f:   # Change to food and name matching
    data = json.load(f)

# Get request for checking the available food


@login_required()
def f_data(request):
    return HttpResponse(data)


# POST IMAGE TO PREDCICT
@csrf_exempt
def predict(request):
    if request.method == "POST":
        f = request.FILES['sentFile']
        file_name = "unnamed.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)

        # load and preprocess the image
        img = plt.imread('/Users/foodpicker/fp/fp_django/'+file_url)
        # img = plt.imread('/home/jhnl/foodpicker/'+file_url)

        # To be changed to 224 when new model is ready
        img = tf.image.resize_with_crop_or_pad(img, 200, 200)

        # Get the predictions and return the top 5
        img = tf.stack([img], axis=0)
        pred = model.predict(img)
        top_5 = heapq.nlargest(5, range(len(pred[0])), key=pred[0].__getitem__)

        print(top_5)
        food = []
        for index, i in enumerate(top_5):
            food.append(food_data.find_one({'ID': i}, {'_id': 0}))
            food[index]['fileName'] = file_name_2

        response = {}
        food.append(file_name_2)
        response['food_predictions'] = food

        # print(file_name_2)
        response['photo_name'] = file_name_2
        print(food[0])
        print(type(food[0]['appearance']))
        return JsonResponse(food, safe=False)
        # return render(request,'homepage.html',response)
        # return response

    else:
        print("Something is wrong.")
        # return render(request,'homepage.html')

# CHOOSE PREDICTIONS AND RENAME/LABEL THE IMAGE
# Assumption: Client send post request with old file name and the food label


@csrf_exempt
def name_photo(request):

    if request.method == 'POST':
        print(request.POST)

        storage = '/Users/foodpicker/fp/fp_django/fp/media/'
        # storage = '/home/jhnl/foodpicker/fp/media/'

        # ensure the photo name will not repeat
        time = '_' + datetime.now().strftime("%d%b%Y%H%S%f")
        old_name = storage + request.POST.get("old_name")
        new = request.POST.get("new_name")
        print(old_name)
        print(new)

        # Move the photo to the corresponding file
        if os.path.exists(storage + new):
            os.rename(old_name, storage + new + '/' + new + time + '.jpg')
        else:
            os.mkdir(storage + new)
            os.rename(old_name, storage + new + '/' + new + time + '.jpg')

        print("Photo renamed from {} to {}".format(old_name, new))

        response = {}
        return JsonResponse(response, safe=False)
        # return render(request,'choose_food.html',response)

    else:
        print('Rename is not working....try again.')


# INPUT A NEW FOOD WHICH MAY OR MAY NOT EXIST IN OTHER OPTIONS
@csrf_exempt
def name_other(request):

    if request.method == 'POST':

        # ensure the photo name will not repeat
        time = '_' + datetime.now().strftime("%d%b%Y%H%S%f")
        storage = '/Users/foodpicker/fp/fp_django/fp/media/'
        # storage = '/home/jhnl/foodpicker/fp/media/'

        old_name = storage + request.POST.get("old_name")
        new = request.POST.get("new_name")
        new = new.replace(' ', '').lower()
        print(old_name)
        print(new)

        # Rename the photo
        os.rename(old_name, storage + 'Other/' + new + time + '.jpg')

        print("New food renamed from {} to {}".format(old_name, new))

        response = {}
        return JsonResponse(response, safe=False)
        # return render(request,'choose_food.html',response)

    else:
        print('Rename is not working....try again.')
    #     return render(request, 'choose_food.html')


# Login page
def user_login(request):
    return HttpResponse("This is the login page.")

# User registration page


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    redirect_field_name = 'fp:login'


# GET FOOD DETAILS/ POST NEW FOOD TO MONGODB
@api_view(['POST', 'GET'])
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
    if request.method == 'POST':
        food_data = JSONParser().parse(request)
        food_serializer = FoodSerializer(data=food_data)
        if food_serializer.is_valid():
            food_serializer.save()
            return JsonResponse(food_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(food_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def food_details(request, label):

    # find food by food_id (id)
    try:
        food = Food.objects.get(label=label)
    except food.DoesNotExist:
        return JsonResponse({'message': 'The food does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the object
    if request.method == 'GET':
        food_serializer = FoodSerializer(food)
        return JsonResponse(food_serializer.data)

    # Update the object (ONLY ALLOW USE TO UPDATE TIPS)
    elif request.method == 'PUT':
        food_data = JSONParser().parse(request)
        food_serializer = FoodSerializer(food, data=food_data)
        if food_serializer.is_valid():
            food_serializer.save()
            return JsonResponse(food_serializer.data)
        return JsonResponse(food_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete an object according to the pk
    # elif request.method == 'DELETE':
    #     Food.delete()
    #     return JsonResponse({'message': 'food was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# User consume food -> add food to user_foodlog
@api_view(['POST'])
def consumed_food(request):

    if request.method == 'POST':
        label = request.POST.get("add_food")
        print(label)
        try:
            food = Food.objects.get(chiName=label)
        except food.DoesNotExist:
            return JsonResponse({'message': 'The food does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # add food log to user_foodlog
    # retrieve nutrient of the food
    # if request.method == 'GET':
        food_serializer = FoodSerializer(food)

        # assign dict to nutrient
        nutrient = food_serializer.data

        nut_tracked = ['protein', 'fat', 'fibre', 'iron', 'iodine',
       'magnesium', 'potassium', 'sodium', 'vitamin_b2', 'vitamin_b12',
       'vitamin_c', 'calcium', 'zinc',
       'vitamin_a']
        
        nutrient = dict([(k,v) for k,v in nutrient.items() if k in nut_tracked])
        nutrient = dict(sorted(nutrient.items(), key=lambda item: item[1], reverse=True))
        # tags = []
        # tags.append([tags for tags, values in nutrient ])

        # consumption = {}
        points = len(nutrient)
        for i in nutrient.keys():
            nutrient[i] = int(points)
            points -= 1

        # assign user and timestamp to the log event
        nutrient['username'] = 'jhnl'
        nutrient['timestamp'] = datetime.now()
        print(nutrient)

        # save to user_foodlog
        user_log.insert(nutrient)
        # return JsonResponse(nutrient)
        return JsonResponse({'message': 'The food has been logged'})


# User check his nutrient status (GET request)
@api_view(['GET'])
def nut_status(request):
    
    # read the food log and write a query to get sum of nutrient values of T-7 to T0
    status = db.fp_user_log.aggregate([
        {'$match': {'username': "jhnl", "timestamp": {
            '$lt': datetime.now(), '$gt': datetime.now() - timedelta(days=7)}}},
        {'$group': {"_id": "$username",
                    "fibre": {"$sum": "$fibre"},
                    "protein": {"$sum": "$protein"},
                    "iron": {"$sum": "$iron"},
                    "vitamin_a": {"$sum": "$vitamin_a"}}},
        {'$project': {'_id':0}}
    ])

    status = list(status)[0]
    return JsonResponse(status)

def check_food_log(request):
    
    status = db.fp_user_log.aggregate([
        {'$match': {'username': "jhnl", "timestamp": {
            '$lt': datetime.now(), '$gt': datetime.now() - timedelta(days=7)}}},
        {'$project': {'_id':0}}
    ])

    status = list(status)
    return JsonResponse(status, safe=False) 
