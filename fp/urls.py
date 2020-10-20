from django.urls import path

# from . import views
from . import views

app_name = 'fp'
urlpatterns = [
    path('', views.predict, name='upload'),
    # path('predict', views.predict, name='predict'),
    path('data', views.food_data, name='all_food'),
]