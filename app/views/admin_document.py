# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm


def admin_document(request):
	try:
		form = AnnouncementUEditorForm(initial={'description': '请在此输入文字'})
	except Exception, e:
		return HttpResponse("创建失败" + str(e))
	return render(request, "admin/admin_document.html", {
		"form": form,
	})
	# form = ItemUEditorModelForm(instance=item)