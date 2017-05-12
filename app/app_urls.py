from django.conf.urls import include, url
from django.views.generic import TemplateView
from views.phone.index import index, map
from views.phone.user import login, logout, information

urlpatterns = [
	url(r'^index/(?P<device_id>\d+)/$', index, name="app_index"),
	url(r'^user/login/$', login, name="app_user_login"),
	url(r'^user/logout/$', logout, name="app_user_logout"),
	url(r'^user/information/$', information, name="app_user_information"),
	url(r'^ranking/$', TemplateView.as_view(template_name="phone/ranking.html")),
	url(r'^map/$', map, name="app_map"),
	url(r'^mine/$', TemplateView.as_view(template_name="phone/mine.html")),
	url(r'^aboutUs/$', TemplateView.as_view(template_name="phone/aboutUs.html")),
	url(r'^knowledge/$', TemplateView.as_view(template_name="phone/knowledge.html")),
]
