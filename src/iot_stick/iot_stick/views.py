from django.views.generic import TemplateView
from tracking.models import ModulePostLog


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['modulelogs'] = ModulePostLog.objects.all()
        context['geom'] = {'lat': -25.363, 'lng': 131.044}
        return context


