from django.urls import path

# from . import views
from . import views

app_name = 'fp'
urlpatterns = [
    path('', views.predict, name='homepage'),
    path('data', views.food_data, name='all_food'),
    # path('upload', views.upload, name='upload'),
    # path('', HomePageView.as_view(), name='home'),
    # path('post/', CreatePostView.as_view(), name='add_post'),
]