from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.app.serializers.task import TaskManagementSerializer
from backend.app.services.ai import AIClient
from backend.app.config.task import system_prompt
from backend.app.utils.json import get_valid_json
from backend.app.models import Task
from typing import List, Dict, Any


class TaskManagementView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = TaskManagementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.input_data = serializer.validated_data

        ai_client = AIClient()

        try:
            result = self.generate_task(ai_client)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_task(self, ai_client):

        tasks = self.list_tasks()
        
        # Initial messages with system prompt and other data
        self.messages = [
            {
                "role": "system",
                "content": (
                    f"{system_prompt} "
                    f" Following are existing tasks: {tasks} \n"
                )
            }
        ] + self.input_data['chat_history'] + [
            {
                "role": "user",
                "content": self.input_data['user_prompt']
            }
        ]

        response = ai_client.send_prompt(messages=self.messages)
        is_valid_json, response_json = get_valid_json(response)

        if is_valid_json:
            self.process_json_data(response_json)
        else:
            self.process_normal_message(response)

        self.remove_system_prompt()
        return self.input_data

    def list_tasks(self) -> List[Dict]:
        task = Task.objects.all()
        return [
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "category": "category",
                "priority": "priority",
                "estimated_time": "estimated_time"
            } for task in task
        ]

    def process_json_data(self, data):
        self.input_data['is_generated'] = True
        action = data["action"]
        task_data = data["data"]

        if action == "create":
            self.create_task(task_data)
        elif action == "update":
            self.update_task(task_data)
        elif action == "delete":
            self.delete_task(task_data)

    def process_normal_message(self, message):
        self.input_data['is_generated'] = False
        self.update_chat_history(
            role="assistant",
            content=message
        )

    def create_task(self, task_data):
        task = Task.objects.create(**task_data)
        self.update_chat_history(
            role="assistant",
            content=(
                f"Task '{task.name}' created successfully. "
                "You can refer to this name to update or delete it in the future."
            )
        )

    def update_task(self, task_data):
        task_name = task_data.pop("name")
        Task.objects.filter(name=task_name).update(**task_data)
        
        self.update_chat_history(
            role="assistant",
            content=(
                f"Task '{task.name}' updated successfully. You can refer to this name to update or delete it in the future."
            )
        )

    def delete_task(self, task_data):
        Task.objects.get(name=task_data["name"]).delete()

        self.update_chat_history(
            role="assistant",
            content=(
                f"Task '{task.name}' deleted successfully.",
            )
        )

    def remove_system_prompt(self):
        self.input_data['chat_history'] = [
            entry for entry in self.input_data['chat_history']
            if entry["role"] != "system"
        ]

    def update_chat_history(self, role, content):
        self.input_data["chat_history"] = self.messages + [
            {
                "role": role,
                "content": content
            }
        ]
