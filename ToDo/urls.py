# ToDo/urls.py
from django.urls import path
from .views import TaskGetView, TaskSaveView, TaskUpdateView, TaskDeleteView, TaskCompleteToggleView, TaskOrderUpdateView, UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('get/', TaskGetView.as_view(), name='task-get'),
    path('save/', TaskSaveView.as_view(), name='task-save'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('complete/<int:pk>/',TaskCompleteToggleView.as_view(), name='complete_task'), 
    path('tasks/update-order/', TaskOrderUpdateView.as_view(), name='task-update-order'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('', views.home, name='home'),  # Define the home view

]
