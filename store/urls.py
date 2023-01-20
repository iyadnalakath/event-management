from django.urls import path
from rest_framework_nested import routers
from .import views

router=routers.DefaultRouter()
router.register('area',views.AreaViewSet)
# router.register('catagory',views.CatagoryViewSet)
router.register('subcatagory',views.SubCatagoryViewSet)
# router.register('event_team',views.EventTeamViewSet)
router.register('service',views.ServiceViewSet)




urlpatterns = router.urls

