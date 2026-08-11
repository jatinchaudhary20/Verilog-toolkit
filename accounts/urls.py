from django.urls import path
from .views import (
                DashboardView, 
                MembersListView, 
                RegisterView, 
                ProfileDetailView, 
                PasswordChangeView, 
                ProfileUpdateView
                )

app_name = 'accounts'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('members', MembersListView.as_view(), name="members-list"),
    path('register/', RegisterView, name='register'),
    path('<int:pk>/user/', ProfileDetailView.as_view(), name='profile-detail'),
    path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile-update'),

    # change password
    path('password-change', PasswordChangeView.as_view(), name='password-change'),
]
