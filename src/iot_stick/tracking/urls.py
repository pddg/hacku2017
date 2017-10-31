from rest_framework import routers
from .views import ModulesViewSets, ModulePostLogViewSets


router = routers.DefaultRouter()
router.register(r'modules', ModulesViewSets)
router.register(r'postlogs', ModulePostLogViewSets)

