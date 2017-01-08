from django.conf.urls import include, url
from views.index import index, index_48, index_average
from views.user import user_login, user_logout
from views.station import station
from views.historical import historical_data_analysis, historical_device, historical_data_list
from views.admin_user import admin_login
from views.admin_user import admin_logout, admin_user_list,admin_user_update,admin_user_info
from views.admin_index import admin_index
from views.admin_data import admin_data, admin_data_update,admin_device_update
from views.admin_document import admin_document_list, admin_document_edit, admin_document_info
from views.platform import information, news_info
urlpatterns = [
	url(r'^$', index_average, name="index_average"),
	url(r'^index/$', index_average, name="index_average"),
	url(r'^index2/$', index_48, name="welcome_48"),
	url(r'^index_old/$', index, name="index"),
	url(r'^station/$', station, name="station"),
	url(r'^historical_device/$', historical_device, name="historical_device"),
	url(r'^historical_device_analysis/(?P<device_id>\d+)/$', historical_data_analysis, name="historical_data_analysis"),
	url(r'^historical_device_data_list/(?P<device_id>\d+)/$', historical_data_list, name="historical_data_list"),
	url(r'^information/$', information, name="information"),
	url(r'^document_info/(?P<news_id>\d+)/$', news_info, name="news_info"),
	url(r'^user_login/$', user_login, name="user_login"),
	url(r'^user_logout/$', user_logout, name="user_logout"),
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
	url(r'^admin_user/info/$', admin_user_info, name="admin_user_info"),
	url(r'^admin_user_list/$', admin_user_list, name="admin_user_list"),
	url(r'^admin_user/update/$', admin_user_update, name="admin_user_update"),
]