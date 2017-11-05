from rest_framework import routers
from .views import ModulesViewSets, ModulePostLogViewSets, ModuleLocationViewSets


router = routers.DefaultRouter()
router.register(r'modules', ModulesViewSets)
router.register(r'postlogs', ModulePostLogViewSets)
router.register(r'location', ModuleLocationViewSets)

