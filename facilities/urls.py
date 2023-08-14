"""
URL configuration for facilities project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from facilities.user.models import User
from facilities.user.viewsets import UserRegistrationView
from . import views
from .views import user_profile #favorite_facilities, adjusting_favorite_facilities
from rest_framework import routers
from facilities.routers import routes as router

urlpatterns = [
    path('get_campsite_data/', views.get_campsite_data),
    path('api/', include((router.urls, 'facilities'), namespace='facilities-api')),
    path('auth/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('protected/profile/', views.user_profile,name='user_profile'),
    # path('profile/', include('django.contrib.auth.urls')),
    # path('protected/profile/favorites/', views.favorite_facilities,name='favorite_facilities'),
    # path('protected/profile/favorites/<int:id>/', views.adjusting_favorite_facilities,name='adjusting_favorite_facilities'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)