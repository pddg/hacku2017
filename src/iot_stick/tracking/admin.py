from django.contrib import admin
from .models import Module, ModulePostLog, ChannelLog

# Register your models here.
admin.site.register(Module)
admin.site.register(ModulePostLog)
admin.site.register(ChannelLog)
