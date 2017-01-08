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
# Create your models here.
