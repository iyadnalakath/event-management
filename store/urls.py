from django.urls import path
from rest_framework_nested import routers
from .import views
from .views import PopularityViewSet

urlpatterns = [
    
    path('popularity/', PopularityViewSet.as_view({'get': 'list'}), name='popularity'),
    path('popularity/<int:pk>', PopularityViewSet.as_view({'get': 'retrieve'}), name='popularity-detail'),
]

router=routers.DefaultRouter()
router.register('area',views.AreaViewSet)
# router.register('catagory',views.CatagoryViewSet)
router.register('subcatagory',views.SubCatagoryViewSet)
# router.register('event_team',views.EventTeamViewSet)
router.register('service',views.ServiceViewSet)
router.register('rating',views.RatingViewSet)
router.register('notification',views.NotificationViewSet)
router.register('enquiry',views.EnquiryViewSet)
router.register('inbox',views.InboxViewSet)






urlpatterns = router.urls + urlpatterns

