# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.models import User, Adminer
from django.contrib.auth.hashers import  check_password, make_password
transform_factor = {"so2": 2949.276785714286, "o3": 2142.7767857142856, "co": 1.2504464285714287, "no2": 2054.017857142857}


@csrf_exempt
def login(request):
	if request.method == "GET":
		return render(request, "phone/login.html", {
		})
	else:
		username = request.POST.get("username")
		password = request.POST.get("password")
		print username, password
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


def logout(request):
	del request.session['username']
	return render(request, "phone/logout.html", {})
