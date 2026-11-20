
from django.urls import path
from . import views
from . import views, schedule_views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("schedule/", schedule_views.schedule, name="schedule"),
]
