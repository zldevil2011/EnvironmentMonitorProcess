# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.models import User
from app.models import Adminer


@csrf_exempt
def admin_login(request):
	# 两级设置，一级管理员查看原始数据和更新数据同时可操作数据，二级管理员查看更新后的数据，发表文章
	if request.method == "GET":
		return render(request, "admin/admin_login.html", {
		})
	else:
		try:
			level = int(request.POST.get("level"))
			username = request.POST.get("username")
			password = request.POST.get("password")
			secret = request.POST.get("secret")
			print level
			print username
			print password
			print secret
			if level == 1:
				try:
					if secret != "123456789":
						return HttpResponse("error")
					user = User.objects.get(username=username)
					print check_password(password, user.password)
					if check_password(password, user.password):
						adminer = Adminer.objects.get(user=user)
						if not user.is_staff:
							return HttpResponse("error")
						request.session["username"] = username
						return HttpResponse("success")
					else:
						return HttpResponse("error")
				except:
					return HttpResponse("error")
			elif level == 2:
				try:
					if secret != "123456":
						return HttpResponse("error")
					user = User.objects.get(username=username)
					print check_password(password, user.password)
					if check_password(password, user.password):
						adminer = Adminer.objects.get(user=user)
						request.session["username"] = username
						return HttpResponse("success")
					else:
						return HttpResponse("error")
				except:
					return HttpResponse("error")
			else:
				return HttpResponse("error")
		except:
			return HttpResponse("error")

@csrf_exempt
def admin_logout(request):
	try:
		del request.session['username']
	except:
		return HttpResponseRedirect("/admin_login/")
	return HttpResponseRedirect("/admin_login/")
	# form = ItemUEditorModelForm(instance=item)