from django.views.generic import TemplateView, DeleteView
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse_lazy
from tracking.models import Module, ModuleLocation, Home
from django.shortcuts import redirect
from tracking.forms import HomeForm, Module


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        modules = [m for m in Module.objects.all() if m.locations.all().count() != 0]
        print(modules)
        latlng = [(m.locations.first().geom.y, m.locations.first().geom.x) for m in modules]
        context['modules'] = modules
        context['init_point'] = {
            'lat': sum([l[0] for l in latlng])/len(latlng),
            'lng': sum([l[1] for l in latlng])/len(latlng),
            'zoom': 15
        }
        return context


class HomeLocationCreateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeLocationCreateView, self).get_context_data(**kwargs)
        context['form'] = HomeForm
        context['geom'] = {
            'lat': 35.048993,
            'lng': 135.779945,
            'zoom': 15
        }
        context['UPDATE'] = False
        return context

    def post(self, request, *args, **kwards):
        name = request.POST.get('name')
        radius = int(request.POST.get('radius'))
        lat = float(request.POST.get('lat'))
        lng = float(request.POST.get('lng'))
        module_id = request.POST.get('module')
        m = Module.objects.get(id=module_id)
        home = Home(
            name=name,
            radius=radius,
            geom=Point(lng, lat, srid=4326),
            module=m
        )
        home.save()
        return redirect('index')


class HomeLocationUpdateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeLocationUpdateView, self).get_context_data(**kwargs)
        h = Home.objects.get(id=self.kwargs['id'])
        context['form'] = HomeForm
        context['geom'] = {
            'lat': h.geom.get_y(),
            'lng': h.geom.get_x(),
            'zoom': 15
        }
        context['UPDATE'] = True
        context['radius'] = h.radius
        context['module_id'] = h.module_id
        context['name'] = h.name
        context['pk'] = h.pk
        return context

    def post(self, request, *args, **kwards):
        h = Home.objects.get(id=self.kwargs['id'])
        h.name = request.POST.get('name')
        h.radius = int(request.POST.get('radius'))
        h.geom.y = float(request.POST.get('lat'))
        h.geom.x = float(request.POST.get('lng'))
        module_id = request.POST.get('module')
        m = Module.objects.get(id=module_id)
        h.module = m
        h.save()
        return redirect('index')


class HomeDeleteView(DeleteView):
    model = Home
    template_name = 'delete_home.html'
    success_url = reverse_lazy('index')
