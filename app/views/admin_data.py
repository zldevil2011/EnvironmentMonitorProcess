# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm


def admin_data(request):
	return render(request, "admin/admin_data.html", {
	})
	# form = ItemUEditorModelForm(instance=item)