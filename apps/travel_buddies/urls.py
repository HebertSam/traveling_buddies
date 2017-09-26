from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^main$', views.main),
    url(r'^travels$', views.dashboard),
    url(r'^destination/(?P<trip_id>\d+)', views.destination),
    url(r'^travels/add$', views.add_trip),
    url(r'^main/registration$', views.registraton),
    url(r'^main/login', views.login),
    url(r'^travels/add/trip', views.create_trip),
    url(r'^logout$', views.logout),
    url(r'^join/(?P<trip_id>\d+)', views.join),
]
