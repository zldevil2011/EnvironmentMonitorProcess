from django.contrib import admin
from app.models import Adminer, Announcement, Project, SensorDatabaseConfig, SensorConfigParameter,Sensor

admin.site.register(Adminer)
admin.site.register(Announcement)
admin.site.register(Project)
admin.site.register(SensorDatabaseConfig)
admin.site.register(SensorConfigParameter)
admin.site.register(Sensor)
# Register your models here.
