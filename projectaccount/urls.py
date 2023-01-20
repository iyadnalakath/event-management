from django.urls import path
from .views import LoginView, RegisterCustomerView,RegisterEventTeamView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('event_team_register/', RegisterEventTeamView.as_view(), name='register'),
]