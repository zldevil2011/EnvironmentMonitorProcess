from django.contrib import admin
from app.models import Adminer, Announcement, Project, SensorDatabaseConfig, SensorConfigParameter,Sensor,Device,WarningRule,WarningEvent,LatestData


class LatestDataAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'aqi', 'pm25', 'pm10', 'so2', 'no2', 'co', 'o3', 'data_time')


class WarningRuleAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'parameter', 'warning_type', 'warning_val')


class WarningEventAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'warning_time')

admin.site.register(Adminer)
admin.site.register(Announcement)
admin.site.register(Project)
admin.site.register(SensorDatabaseConfig)
admin.site.register(SensorConfigParameter)
admin.site.register(Sensor)
admin.site.register(Device)
admin.site.register(WarningRule, WarningRuleAdmin)
admin.site.register(WarningEvent, WarningEventAdmin)
admin.site.register(LatestData, LatestDataAdmin)
# Register your models here.
