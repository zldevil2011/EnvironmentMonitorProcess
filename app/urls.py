from django.conf.urls import include, url
from views.index import index_all, index_48, index_average
from views.user import user_login, user_logout
from views.station import station, station_ranking
from views.historical import historical_data_analysis, historical_device, historical_data_list, historical_voltage_list,device_data_map
from views.admin_user import admin_login
from views.admin_user import admin_logout, admin_user_list,admin_user_update,admin_user_info
from views.admin_index import admin_index
from views.admin_data import admin_data, admin_data_update,admin_device_update
from views.admin_document import admin_document_list, admin_document_edit, admin_document_info
from views.platform import information, news_info
from views.msp_server import msp_login
from views.msp_server import msp_logout
from views.msp_server import msp_sendto
from views.msp_server import msp_receive_data
from views.msp_server import msp_receive_log
from views.utils.data_export import historical_device_data_export
from views.utils.data_export import historical_device_data_export_function

from views.server import server_index
from views.server import server_device_add
from views.server import server_device_parameter
from views.server import server_project_sensor_config
from views.server import server_device_data
from views.server import server_device_data_list
from views.server import server_sensor_list
from views.server import server_device_info
from views.server import server_data_log
from views.server import server_device_eui


urlpatterns = [
	url(r'^$', index_average, name="index_average"),
	url(r'^index/$', index_average, name="index_average"),
	url(r'^voltage/$', historical_voltage_list, name="historical_voltage_list"),
	url(r'^index2/$', index_48, name="welcome_48"),
	url(r'^index_old/$', index_all, name="index_all"),
	url(r'^station/$', station, name="station"),
	url(r'^station_ranking/$', station_ranking, name="station_ranking"),
	url(r'^historical_device/$', historical_device, name="historical_device"),
	url(r'^device_data_map/$', device_data_map, name="device_data_map"),
	url(r'^historical_device_analysis/(?P<device_id>\d+)/$', historical_data_analysis, name="historical_data_analysis"),
	url(r'^historical_device_data_list/(?P<device_id>\d+)/$', historical_data_list, name="historical_data_list"),
	url(r'^information/$', information, name="information"),
	url(r'^document_info/(?P<news_id>\d+)/$', news_info, name="news_info"),
	url(r'^user_login/$', user_login, name="user_login"),
	url(r'^user_logout/$', user_logout, name="user_logout"),

	url(r'^historical_device_data_export/$', historical_device_data_export, name="historical_device_data_export"),
	url(r'^historical_device_data_export/(?P<device_id>\d+)/$', historical_device_data_export_function, name="historical_device_data_export_function"),


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

urlpatterns += [
	url(r'^msp_login/$', msp_login, name="msp_login"),
	url(r'^msp_logout/$', msp_logout, name="msp_logout"),
	url(r'^msp_sendto/$', msp_sendto, name="msp_sendto"),
	url(r'^msp_receive_data/$', msp_receive_data, name="msp_receive_data"),
	url(r'^msp_receive_log/$', msp_receive_log, name="msp_receive_log"),
]

urlpatterns += [
	url(r'^server_index/$', server_index, name="server_index"),
	url(r'^server_device_add/$', server_device_add, name="server_device_add"),
	url(r'^server_device_parameter/$', server_device_parameter, name="server_device_parameter"),
	url(r'^server_project_sensor_config/$', server_project_sensor_config, name="server_project_sensor_config"),
	url(r'^server_device_data/$', server_device_data, name="server_device_data"),
	url(r'^server_sensor_list/$', server_sensor_list, name="server_sensor_list"),
	url(r'^server_device_data_list/$', server_device_data_list, name="server_device_data_list"),
	url(r'^server_device_info/$', server_device_info, name="server_device_info"),
	url(r'^server_data_log/$', server_data_log, name="server_data_log"),
	url(r'^server_device_eui/$', server_device_eui, name="server_device_eui"),
]