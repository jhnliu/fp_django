from django.urls import path

from . import views

app_name = 'fp'
urlpatterns = [
    path('', views.food_data, name='all_food'),
    path('', views.predict, name='prediction'),
]