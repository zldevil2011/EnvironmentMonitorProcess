from django.conf.urls import include, url
from views.index import index
from views.station import station
from views.historical import historical_data, historical_device
from views.admin_user import admin_login
from views.admin_user import admin_logout
from views.admin_index import admin_index
from views.admin_data import admin_data
from views.admin_document import admin_document
from views.platform import information
urlpatterns = [
	url(r'^$', index, name="welcome"),
	url(r'^index/$', index, name="welcome"),
	url(r'^station/$', station, name="station"),
	url(r'^historical_device/$', historical_device, name="historical_device"),
	url(r'^historical_device_data/(?P<device_id>\d+)/$', historical_data, name="historical_data"),
	url(r'^information/$', information, name="information")
]

urlpatterns += [
	url(r'^admin_login/$', admin_login, name="admin_login"),
	url(r'^admin_logout/$', admin_logout, name="admin_logout"),
	url(r'^admin_index/$', admin_index, name="admin_index"),
	url(r'^admin_data/$', admin_data, name="admin_data"),
	url(r'^admin_document/$', admin_document, name="admin_document"),
]