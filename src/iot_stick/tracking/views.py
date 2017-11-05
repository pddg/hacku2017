from rest_framework import viewsets
from django.views.generic import TemplateView
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
    queryset = ModuleLocation.objects.order_by('-created_on').all()
    serializer_class = ModuleLocationSerializer
    filter_fields = ('module',)
    distance_filter_field = 'geom'
    distance_filter_convert_meters = True


class ModuleDetailView(TemplateView):
    template_name = 'tracking/module-detail.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleDetailView, self).get_context_data(**kwargs)
        m = Module.objects.get(id=self.kwargs['id'])
        context['module'] = {
            'id': m.pk,
            'module_id': m.module_id
        }
        locations = m.locations.order_by('-created_on').all()
        context['init_point'] = {
            'lat': locations[0].geom.y,
            'lng': locations[0].geom.x,
            'zoom': 16
        }
        context['locations'] = []
        for loc in locations:
            context['locations'].insert(0, {
                'lat': loc.geom.y,
                'lng': loc.geom.x,
                'created_on': loc.created_on.strftime('%Y/%m/%d %H:%M:%S.%f')
            })
        return context
