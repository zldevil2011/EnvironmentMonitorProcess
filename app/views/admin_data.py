# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from app.models import Adminer


def admin_data(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	return render(request, "admin/admin_data.html", {
	})
	# form = ItemUEditorModelForm(instance=item)