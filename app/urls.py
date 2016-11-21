from django.conf.urls import include, url
from views.index import index
from views.station import station
from views.historical import historical_data, historical_device
from views.admin_index import admin_index
from views.admin_data import admin_data
from views.platform import information
urlpatterns = [
	url(r'^$', index, name="welcome"),
	url(r'^index/$', index, name="welcome"),
	url(r'^station/$', station, name="station"),
	url(r'^historical_device/$', historical_device, name="historical_device"),
	url(r'^historical_device_data/$', historical_data, name="historical_data"),
	url(r'^information/$', information, name="information")
]

urlpatterns += [
	url(r'^admin_index/$', admin_index, name="admin_index"),
	url(r'^admin_data/$', admin_data, name="admin_data"),
]