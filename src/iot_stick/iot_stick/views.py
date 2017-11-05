from django.views.generic import TemplateView
from django.contrib.gis.geos import Point
from tracking.models import Module, ModuleLocation, Home
from django.shortcuts import redirect
from tracking.forms import HomeForm, Module


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['modules'] = Module.objects.all()
        context['geom'] = {'lat': -25.363, 'lng': 131.044, 'zoom': 15}
        return context


class HomeLocationCreateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeLocationCreateView, self).get_context_data(**kwargs)
        context['form'] = HomeForm
        context['geom'] = {'lat': 35.048993, 'lng': 135.779945, 'zoom': 15}
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


