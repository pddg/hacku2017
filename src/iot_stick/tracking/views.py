import django_filters
from rest_framework import viewsets, filters
from .models import Module, ModulePostLog
from .serializer import ModuleSerializer, ModulePostLogSerializer


class ModulesViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModulePostLogViewSets(viewsets.ModelViewSet):
    queryset = ModulePostLog.objects.all()
    serializer_class = ModulePostLogSerializer
    filter_fields = ('module', 'type')
