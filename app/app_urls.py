from django.conf.urls import include, url
from django.views.generic import TemplateView


urlpatterns = [
	url(r'^index/$', TemplateView.as_view(template_name="phone/index.html")),
	url(r'^ranking/$', TemplateView.as_view(template_name="phone/ranking.html")),
]
