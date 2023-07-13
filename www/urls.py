"""
URL configuration for www project.

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from www.conference_rooms.views import ReservationViewSet
from www.conference_rooms.views import main_view, create_reservations, room_status, reserve_room

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', main_view, name='main'),
    path('reservations/', create_reservations, name='create_reservations'),
    path('room_status/', room_status, name='room_status'),
    path('reserve_room/<int:room_id>/', reserve_room, name='reserve_room'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
