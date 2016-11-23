# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from app.models import Adminer


def admin_index(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	try:
		form = AnnouncementUEditorForm(initial={'description': '请在此输入文字'})
	except Exception, e:
		return HttpResponse("创建失败" + str(e))
	return render(request, "admin/admin_index.html", {
		"form": form,
	})
	# form = ItemUEditorModelForm(instance=item)