from django.conf.urls import include, url
from views.welcome import welcome
from views.station import station
urlpatterns = [
	url(r'^welcome/$', welcome, name="welcome"),
	url(r'^station/$', station, name="station")
]