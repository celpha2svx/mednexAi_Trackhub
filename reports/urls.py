from django.urls import path
from .views import SubmitReportView, FeedView, MentorDashboardView

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='submit'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('dashboard/', MentorDashboardView.as_view(), name='dashboard'),
]
