# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from django.contrib.auth.hashers import  check_password, make_password
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


@csrf_exempt
def admin_user_list(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	user_list_1 = Adminer.objects.filter(user__is_staff=True)
	user_list_2 = Adminer.objects.filter(user__is_staff=False)
	return render(request, "admin/admin_user.html", {
		"user_list_1":user_list_1,
		"user_list_2":user_list_2,
		"adminer": adminer,
	})


@csrf_exempt
def admin_user_update(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	add = request.POST.get("add", None)
	delete = request.POST.get("delete", None)
	modify = request.POST.get("modify", None)
	print add
	print delete
	print modify
	if add is not None:
		username = request.POST.get("username", None)
		password = request.POST.get("password", None)
		level = request.POST.get("level", None)
		if username is None or username == "" or password is None or password == "" or level is None:
			return HttpResponse("error")
		try:
			adminer_t = Adminer.objects.get(username=username)
			return HttpResponse("error")
		except Adminer.DoesNotExist:
			secret_password = make_password(password, None, 'pbkdf2_sha256')
			user = User()
			user.username = username
			user.password = secret_password
			if int(level) == 1:
				user.is_staff = True
			user.save()
			adminer_new = Adminer()
			adminer_new.username = username
			adminer_new.user = user
			adminer_new.save()
			return HttpResponse("success")
	elif delete is not None:
		try:
			user_id = int(request.POST.get("user_id"))
		except:
			return HttpResponse("error")
		try:
			adminer_del = Adminer.objects.get(pk=user_id)
			adminer_del.user.delete()
			adminer_del.delete()
			return HttpResponse("success")
		except:
			return HttpResponse("error")
	elif modify is not None:
		password = request.POST.get("password", None)
		if password is None or password == "":
			return HttpResponse("error")
		try:
			user_id = int(request.POST.get("user_id"))
			adminer_modify = Adminer.objects.get(pk=user_id)
			secret_password = make_password(password, None, 'pbkdf2_sha256')
			adminer_modify.user.password = secret_password
			adminer_modify.user.save()
			return HttpResponse("success")
		except:
			return HttpResponse("error")
	else:
		return HttpResponse("error")


def admin_user_info(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	return render(request, "admin/admin_user_info.html", {
		"adminer": adminer,
	})

