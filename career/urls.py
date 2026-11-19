from django.urls import path
from . import views

app_name = "career"
urlpatterns = [
    path("", views.index, name="index"),
    path("field/<slug:field_id>/", views.field_detail, name="field"),
    path("major/<slug:major_id>/", views.major_detail, name="major"),
    path("job/<slug:job_id>/", views.job_detail, name="job"),
]
