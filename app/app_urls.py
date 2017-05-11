from django.conf.urls import include, url
from django.views.generic import TemplateView
from views.phone.index import index

urlpatterns = [
	url(r'^index/(?P<device_id>\d+)/$', index, name="app_index"),
	url(r'^ranking/$', TemplateView.as_view(template_name="phone/ranking.html")),
	url(r'^map/$', TemplateView.as_view(template_name="phone/map.html")),
	url(r'^mine/$', TemplateView.as_view(template_name="phone/mine.html")),
]
