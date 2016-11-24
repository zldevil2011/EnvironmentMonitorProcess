from django.conf.urls import include, url
from views.index import index
from views.station import station
from views.historical import historical_data, historical_device
from views.admin_user import admin_login
from views.admin_user import admin_logout, admin_user_list,admin_user_update
from views.admin_index import admin_index
from views.admin_data import admin_data, admin_data_update,admin_device_update
from views.admin_document import admin_document_list, admin_document_edit, admin_document_info
from views.platform import information, news_info
urlpatterns = [
	url(r'^$', index, name="welcome"),
	url(r'^index/$', index, name="welcome"),
	url(r'^station/$', station, name="station"),
	url(r'^historical_device/$', historical_device, name="historical_device"),
	url(r'^historical_device_data/(?P<device_id>\d+)/$', historical_data, name="historical_data"),
	url(r'^information/$', information, name="information"),
	url(r'^document_info/(?P<news_id>\d+)/$', news_info, name="news_info"),
]

urlpatterns += [
	url(r'^admin_login/$', admin_login, name="admin_login"),
	url(r'^admin_logout/$', admin_logout, name="admin_logout"),
	url(r'^admin_index/$', admin_index, name="admin_index"),
	url(r'^admin_data/$', admin_data, name="admin_data"),
	url(r'^admin_data/update/$', admin_data_update, name="admin_data_update"),
	url(r'^admin_data/device/update/$', admin_device_update, name="admin_device_update"),
	url(r'^admin_document_edit/$', admin_document_edit, name="admin_document"),
	url(r'^admin_document_list/$', admin_document_list, name="admin_document"),
	url(r'^admin_document_info/(?P<news_id>\d+)/$', admin_document_info, name="admin_document_info"),
	url(r'^admin_user_list/$', admin_user_list, name="admin_user_list"),
	url(r'^admin_user/update/$', admin_user_update, name="admin_user_update"),
]