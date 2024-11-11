#views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
import json



# View to get all tasks for the logged-in user
class TaskGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only get tasks that belong to the logged-in user
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# View to save a new task for the logged-in user
class TaskSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user to the logged-in user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to update an existing task that belongs to the logged-in user
class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            # Ensure that the task belongs to the logged-in user
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to update it."},
                            status=status.HTTP_404_NOT_FOUND)
        
        # Allow partial updates to enable toggling 'complete' status
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to delete a task that belongs to the logged-in user
class TaskDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            # Ensure that the task belongs to the logged-in user
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to delete it."},
                            status=status.HTTP_404_NOT_FOUND)
        
        task.delete()
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class TaskCompleteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            # Ensure that the task belongs to the logged-in user
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to update it."},
                            status=status.HTTP_404_NOT_FOUND)
        
        # Toggle the 'complete' status of the task
        task.complete = not task.complete
        task.save()
        
        # Return the updated task data
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TaskOrderUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        tasks = request.data.get('tasks', [])
        if not tasks:
            return Response({"error": "No tasks provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for task_data in tasks:
                task_id = task_data.get('id')
                order = task_data.get('order')

                # Ensure that the task belongs to the logged-in user
                task = Task.objects.get(pk=task_id, user=request.user)
                task.order = order
                task.save()

            return Response({"message": "Task order updated successfully."}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to update it."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # User Registration View
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        try:
            # Extract data from the request
            data = request.data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

            # Create and save the user
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Ensure the password is hashed
            )
            user.save()

            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)