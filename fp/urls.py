from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


# from . import views
from .views import *

app_name = 'fp'
urlpatterns = [
    path('predict/', predict, name='predict'),
    path('name_photo/', name_photo, name='name_photo'),
    path('name_other/', name_other, name='name_other'),
    path('consumed_food/', consumed_food, name='consumed_food'),
    path('nut_status/', nut_status, name='check nutrient status'),
    path('check_food_log/', check_food_log, name='check food log'),
    # path('variety', views.variety, name='variety'),
    # path('origin', views.origin, name='origin'),
    path('data/', f_data, name='all_food'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='templates/login.html'), name='user-login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    re_path(r'^food_list', food_list),
    re_path(r'^food_detail/(?P<label>[0-9A-z]+)$', food_details),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)