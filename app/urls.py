from django.conf.urls import include, url
from views.index import index
from views.station import station
from views.historical import historical_data
urlpatterns = [
	url(r'^index/$', index, name="welcome"),
	url(r'^station/$', station, name="station"),
	url(r'^historical/$', historical_data, name="station")
]