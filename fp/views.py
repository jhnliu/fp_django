
# Load required package from django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 

# Load packages for tf
import os
import json
import heapq
# import pymongo
import traceback
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
# from .models import Post
# from .forms import PostForm

# Load tensorflow model
model = tf.keras.models.load_model('fp/src/13Oct_62food')
print("Successfully loaded model")

# Connect to DB

with open('fp/src/food_data.json', 'r') as f:
    data = json.load(f)

def food_data(request):
    return HttpResponse(data)

def upload(request):
    return render(request, 'homepage.html')

def predict(request):
    if  request.method == "POST":
        f=request.FILES['sentFile']
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)

        # load and preprocess the image
        img = plt.imread('/Users/foodpicker/fp/fp_django'+file_url)

        # Change the directory to ubuntu
        # img = plt.imread('/projects/django'+file_url)

        img = tf.image.resize_with_crop_or_pad(img, 200,200)
        img = tf.stack([img], axis=0)

        # Get the predictions and return the top 5
        pred = model.predict(img)
        top_5 = heapq.nlargest(5, range(len(pred[0])), key=pred[0].__getitem__)

        food = []
        for i in top_5:
            food.append(data[i])
        response['name'] = str(food)
        # return JsonResponse(food, safe=False)
        return render(request,'homepage.html',response)

    else:
        print("Something is wrong in the predic views.")
        # return render(request,'homepage.html')


# class HomePageView(ListView):
#     model = Post
#     template_name = 'home.html'

# class CreatePostView(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'post.html'
#     success_url = reverse_lazy('fp:home')