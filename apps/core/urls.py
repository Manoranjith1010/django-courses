from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.profile, name="profile"),
    path('update/', views.update_profile, name="update-profile"),
    path('save/', views.save_profile, name="save-profile"),
]
