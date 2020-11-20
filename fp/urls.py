from django.urls import path

# from . import views
from . import views

app_name = 'fp'
urlpatterns = [
    path('predict', views.predict, name='predict'),
    # path('variety', views.variety, name='variety'),
    # path('origin', views.origin, name='origin'),
    path('data', views.food_data, name='all_food'),
]