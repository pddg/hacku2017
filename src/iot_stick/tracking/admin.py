from django.contrib.gis import admin
from .models import Module, ModulePostLog, ChannelLog, ModuleLocation

# Register your models here.
admin.site.register(Module)
admin.site.register(ModulePostLog)
admin.site.register(ChannelLog)
admin.site.register(ModuleLocation, admin.OSMGeoAdmin)
