import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import *
from .serializers import *
from .utils.firebase import (
    send_notification_to_device,
    send_notification_to_devices
)
from .models import Notification
class LogView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # Paths to the log files
        info_log_file = os.path.join(settings.BASE_DIR, 'logs/logs', 'info.log')
        logs = []
        try:
            # Read the info log file if it exists
            if os.path.exists(info_log_file):
                with open(info_log_file, 'r', encoding='utf-8') as f:
                    logs.extend(f.readlines())  # Add the info logs to the list
            else:
                logs.append("Info log file does not exist.")
            # Only return the last 100 logs for performance reasons
            logs = logs[-100:]
            return Response({"logs": logs})
        except Exception as e:
            # Log the exception and return a user-friendly message
            return Response({"error": "An error occurred while retrieving the logs."}, status= 500)



class FrontendLogView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FrontendLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Log created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        logs = FrontendLog.objects.all().order_by('-created_at')
        serializer = FrontendLogSerializer(logs, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)




class NotificationHistoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        notifications = Notification.objects.all().order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    

    def NotificationDeleteView(self, request):
        print("Deleting notifications " ,request.query_params)
        notif_id = request.query_params.get('id', None)
        if notif_id:
            try:
                notification = Notification.objects.get(id=notif_id)
                notification.delete()
                return Response({"message": f"Notification {notif_id} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Notification.DoesNotExist:
                return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            Notification.objects.all().delete()
            return Response({"message": "All notifications deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class NotificationDeleteView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request):
            print("Deleting notifications " ,request.query_params)
            notif_id = request.query_params.get('id', None)
            if notif_id:
                try:
                    notification = Notification.objects.get(id=notif_id)
                    notification.delete()
                    return Response({"message": f"Notification {notif_id} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                except Notification.DoesNotExist:
                    return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                Notification.objects.all().delete()
                return Response({"message": "All notifications deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class NotificationToDeviceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        device_token = request.data.get("deviceToken")
        title = request.data.get("title")
        message = request.data.get("message")
        data = request.data.get("data", {})
        reportUuid = request.data.get("reportUuid", "")

        try:
            response = send_notification_to_device.send_to_device(device_token, title, message, data)
            Notification.objects.create(
                title=title,
                message=message,
                reportUuid=reportUuid,
                # isRead defaults to False, created_at auto-set
            )
            return Response({"success": True, "response": str(response)}, status=200)
        except Exception as e:
            # Log failed notification with minimal info
            Notification.objects.create(
                title=title,
                message=message,
                reportUuid=reportUuid,
            )
            return Response({"success": False, "error": str(e)}, status=500)

class NotificationDeleteView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, id=None):
        print("Deleting notifications", id)
        if id:
            try:
                notification = Notification.objects.get(id=id)
                notification.delete()
                return Response({"message": f"Notification {id} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Notification.DoesNotExist:
                return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            Notification.objects.all().delete()
            return Response({"message": "All notifications deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class NotificationMarkAsReadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request  , id=None):
        print("Marking notification as read", id)   
        if not id:
            return Response({"error": "Notification ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            notification = Notification.objects.get(id=id)
            notification.isRead = True
            notification.save()
            return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)


class NotificationToDevicesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        device_tokens = request.data.get("deviceTokens", [])
        title = request.data.get("title")
        message = request.data.get("message")
        data = request.data.get("data", {})
        reportUuid = request.data.get("reportUuid", "")

        try:
            response = send_notification_to_devices.send_to_devices(device_tokens, title, message, data)
            return Response({"success": True, "response": str(response)}, status=200)
        except Exception as e:
            Notification.objects.create(
                title=title,
                message=message,
                reportUuid=reportUuid,
            )
            return Response({"success": False, "error": str(e)}, status=500)


class NotificationToTopicView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        topic = request.data.get("topic")
        title = request.data.get("title")
        message = request.data.get("message")
        reportUuid = request.data.get("reportUuid", "")

        try:
            response = send_notification_to_devices.send_to_topic(topic, title, message, reportUuid)
            Notification.objects.create(
                title=title,
                message=message,
                reportUuid=reportUuid,
            )
            return Response({"response": str(response)}, status=200)
        except Exception as e:
            Notification.objects.create(
                title=title,
                message=message,
                reportUuid=reportUuid,
            )
            return Response({"success": False, "error": str(e)}, status=500)