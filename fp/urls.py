from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


# from . import views
from .views import *

app_name = 'fp'
urlpatterns = [
    path('fp/predict/', predict, name='predict'),
    path('fp/name_photo/', name_photo, name='name_photo'),
    # path('variety', views.variety, name='variety'),
    # path('origin', views.origin, name='origin'),
    path('fp/data/', f_data, name='all_food'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='user-login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    re_path(r'^api/fp$', food_list),
    re_path(r'^api/fp/(?P<food_id>[a-zA-Z0-9]+)$', food_details),
    re_path(r'^api/fp/published$', food_list_published)
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)