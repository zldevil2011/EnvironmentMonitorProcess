# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm


def admin_login(request):
	# 两级设置，一级管理员查看原始数据和更新数据同时可操作数据，二级管理员查看更新后的数据，发表文章
	return render(request, "admin/admin_data.html", {
	})
	# form = ItemUEditorModelForm(instance=item)