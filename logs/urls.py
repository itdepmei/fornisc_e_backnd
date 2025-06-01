from django.urls import path
from .views import *

urlpatterns = [
    path("logs/", LogView.as_view(), name="log-view"),
    path("frontend-logs/", FrontendLogView.as_view(), name="frontend-logs"),
    path(
        "notifications/history/",
        NotificationHistoryView.as_view(),
        name="notification-history",
    ),
    path(
        "notifications/device/",
        NotificationToDeviceView.as_view(),
        name="notification-device",
    ),
    path(
        "notifications/devices/",
        NotificationToDevicesView.as_view(),
        name="notification-devices",
    ),
    path(
        "notifications/topic/",
        NotificationToTopicView.as_view(),
        name="notification-topic",
    ),
    # 🔥 Delete a specific notification by ID
    path("notifications/delete/<int:id>/",
     NotificationDeleteView.as_view(), name="notification-delete"),

     path("notifications/mark-read/<int:id>/", NotificationMarkAsReadView.as_view(), name="notification-mark-read"),
]