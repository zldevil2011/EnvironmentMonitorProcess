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
def user_login(request):
	if request.method == "GET":
		return render(request, "app/user_login.html", {
		})
	else:
		try:
			username = request.POST.get("username")
			password = request.POST.get("password")
			print username
			print password
			try:
				user = User.objects.get(username=username)
				print check_password(password, user.password)
				if check_password(password, user.password):
					adminer = Adminer.objects.get(user=user)
					request.session["username"] = username
					request.session.set_expiry(0)
					return HttpResponse("success")
				else:
					return HttpResponse("error")
			except:
				return HttpResponse("error")
		except:
			return HttpResponse("error")


@csrf_exempt
def user_logout(request):
	try:
		del request.session['username']
	except:
		return HttpResponseRedirect("/user_login/")
	return HttpResponseRedirect("/user_login/")