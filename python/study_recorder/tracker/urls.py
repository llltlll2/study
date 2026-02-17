from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.GoalCreateView.as_view(), name='goal_create'),
    path('goal/<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
    path('goal/<int:goal_id>/record/add/', views.StudyRecordCreateView.as_view(), name='record_create'),
]
