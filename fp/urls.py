from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# from . import views
from .views import *

app_name = 'fp'
urlpatterns = [
    path('predict', predict, name='predict'),
    path('success', success, name='success'),
    # path('variety', views.variety, name='variety'),
    # path('origin', views.origin, name='origin'),
    path('data', food_data, name='all_food'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)