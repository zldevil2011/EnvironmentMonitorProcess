from django.contrib import admin
from app.models import Adminer, Announcement, Project, SensorDatabaseConfig, SensorConfigParameter,Sensor,Device,WarningRule,WarningEvent,LatestData

admin.site.register(Adminer)
admin.site.register(Announcement)
admin.site.register(Project)
admin.site.register(SensorDatabaseConfig)
admin.site.register(SensorConfigParameter)
admin.site.register(Sensor)
admin.site.register(Device)
admin.site.register(WarningRule)
admin.site.register(WarningEvent)
admin.site.register(LatestData)
# Register your models here.
