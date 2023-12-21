from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.GetProfileAPIView.as_view(), name="get-profile"),
    path(
        "<str:username>/update/",
        views.ProfileUpdateAPIView.as_view(),
        name="update-profile",
    ),
    path("agents/all/", views.AgentListAPIView.as_view(), name="agent-list"),
    path("top-agents/", views.TopAgentsListAPIView.as_view(), name="top-agent-list"),
    # path('profile/<int:pk>/', views.ProfileRetrieveAPIView.as_view(), name='profile-detail'),
    # path('profile/<int:pk>/delete/', views.ProfileDeleteAPIView.as_view(), name='delete-profile-detail'),
    # path('profile/<int:pk>/listings/', views.ProfileListingsAPIView.as_view(), name='profile-listings'),
]
