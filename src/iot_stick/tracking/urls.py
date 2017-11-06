from django.conf.urls import url
from rest_framework import routers
from .views import (
    ModulesViewSets,
    ModulePostLogViewSets,
    ModuleLocationViewSets,
    ModuleDetailView,
    HomeViewSets
)


router = routers.DefaultRouter()
router.register(r'modules', ModulesViewSets)
router.register(r'postlogs', ModulePostLogViewSets)
router.register(r'location', ModuleLocationViewSets)
router.register(r'home', HomeViewSets)

urlpatterns = [
    url(r'^module/(?P<id>\d+)/$', ModuleDetailView.as_view(), name='module')
]

