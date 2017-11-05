from rest_framework import viewsets
from .models import Module, ModulePostLog, ModuleLocation
from .serializer import ModuleSerializer, ModulePostLogSerializer, ModuleLocationSerializer


class ModulesViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModulePostLogViewSets(viewsets.ModelViewSet):
    queryset = ModulePostLog.objects.all()
    serializer_class = ModulePostLogSerializer
    filter_fields = ('module', 'type')


class ModuleLocationViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleLocation.objects.all()
    serializer_class = ModuleLocationSerializer
    filter_fields = ('module',)
    distance_filter_field = 'geom'
    distance_filter_convert_meters = True
