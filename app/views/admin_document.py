# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dss.Serializer import serializer
import json
from app.forms import AnnouncementUEditorForm, AnnouncementUEditorModelForm
from app.models import Adminer, Announcement
from datetime import datetime
import time

def admin_document_list(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	news_list = Announcement.objects.all()
	return render(request, "admin/admin_document_list.html", {
		"adminer": adminer,
		"document_list": news_list,
	})


@csrf_exempt
def admin_document_edit(request):
	try:
		adminer = Adminer.objects.get(username=request.session["username"])
	except:
		return HttpResponseRedirect("/admin_login/")
	print request.method
	if request.method == "POST":
		title = request.POST.get("title", None)
		content = request.POST.get("content", None)
		try:
			news_id = int(request.POST.get("news_id"))
		except:
			news_id = None
		delete_tag = request.POST.get("delete_tag", None)
		print title
		print content
		print news_id
		print delete_tag
		if delete_tag is None:
			if title is None or content is None:
				return HttpResponse("error")
			# 新建news
			if news_id is None or news_id == "":
				print news_id
				try:
					news = Announcement()
					news.title = title
					news.content = content
					news.author = adminer.username
					news.date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
					news.time = time.strftime('%H:%M:%S',time.localtime())
					news.read_count = 0
					news.save()
					print "okokoko"
					return HttpResponse("success")
				except:
					print "not ok not ok"
					return HttpResponse("error")
			# 更新news 内容
			else:
				try:
					news = Announcement.objects.get(pk=int(news_id))
					news.title = title
					news.content = content
					news.author = adminer.username
					news.save()
					return HttpResponse("success")
				except Exception, e:
					print(str(e))
					return HttpResponse("error")
		# 删除news
		else:
			if news_id is None:
				return HttpResponse("error")
			try:
				news = Announcement.objects.get(pk=int(news_id))
				news.delete()
				return HttpResponse("success")
			except:
				return HttpResponse("error")

	elif request.method == "GET":
		try:
			news_id = int(request.GET.get("nid", -1))
			news = Announcement.objects.get(pk=news_id)
			# form = AnnouncementUEditorModelForm(instance=news)
			form = AnnouncementUEditorForm(initial={'description': '请在此输入文字'})
		except Exception, e:
			print str(e)
			form = AnnouncementUEditorForm(initial={'description': '请在此输入文字'})
			news = None
		print(form)
		return render(request, "admin/admin_document.html", {
			"form": form,
			"adminer":adminer,
			"news": news,
		})
	# form = ItemUEditorModelForm(instance=item)