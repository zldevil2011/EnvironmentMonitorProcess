#encoding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Adminer(models.Model):
	user = models.OneToOneField(User, related_name='appuser')
	username = models.CharField(max_length=50, null=True)
	admin_node = models.CommaSeparatedIntegerField(null=True, max_length=500)
	def __unicode__(self):
		return str(self.pk)


class Announcement(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	read_count = models.IntegerField(default=0)
	content = models.TextField(default='')

	def __unicode__(self):
		return str(self.pk)


# 项目信息
class Project(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return str(self.pk)


# 设备信息
class Device(models.Model):
	num = models.IntegerField(default=0)
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=500, null=True)
	install_time = models.DateTimeField(null=True)
	project_id = models.IntegerField(default=0)


# 参数数据库配置
class SensorDatabaseConfig(models.Model):
	project_id = models.IntegerField(default=0)
	name = models.CharField(max_length=200, null=True)
	code = models.IntegerField(default=0)
	val = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return str(self.pk)


# 传感器参数解析系数
class SensorConfigParameter(models.Model):
	project_id = models.IntegerField(default=0)
	name = models.CharField(max_length=200, null=True)
	code = models.IntegerField(default=0)
	val = models.FloatField(default=1)

	def __unicode__(self):
		return str(self.pk)


# 传感器信息
class Sensor(models.Model):
	name = models.CharField(max_length=200, null=True)
	code = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.pk)

# Create your models here.
