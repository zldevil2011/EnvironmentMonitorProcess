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
	dev_eui = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return str(self.num)


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


# 报警规则
class WarningRule(models.Model):
	device_id = models.IntegerField(default=0)				# 对应的设备ID
	parameter = models.CharField(max_length=200, null=True) # 关注的参数（aqi,pm25,pm10,so2,no2,co,o3）
	warning_type = models.IntegerField(default=0)			# 0代表数值，1代表百分比
	warning_val = models.FloatField(default=0.0)			# 0代表数值，1代表百分比

	def __unicode__(self):
		return str(self.pk)


# 每台设备的最新数据
class LatestData(models.Model):
	device_id = models.IntegerField(default=0)				# 设备ID
	aqi = models.FloatField(default=0.0)					# AQI指数
	pm25 = models.FloatField(default=0.0)					# Pm2.5浓度
	pm10 = models.FloatField(default=0.0)					# Pm10浓度
	so2 = models.FloatField(default=0.0)					# So2浓度
	no2 = models.FloatField(default=0.0)					# No2浓度
	co = models.FloatField(default=0.0)						# Co浓度
	o3 = models.FloatField(default=0.0)						# O3浓度
	data_time = models.DateTimeField(null=True)				# 数据采集时间

	def __unicode__(self):
		return str(self.pk)


# 报警
class WarningEvent(models.Model):
	device_id = models.IntegerField(default=0)
	content = models.CharField(max_length=200, null=True)
	warning_time = models.DateTimeField(null=True)
	read_tag = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.pk)
# Create your models here.
