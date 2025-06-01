from django.urls import path
from .views import *
urlpatterns = [
    path('incidents/', IncindentView.as_view(), name='incident-list-create'),
    path('incidents/<str:uuid>/', IncindentView.as_view(), name='incident-detail'),
    # retrieve all evidence
    path('evidence/', EvidenceView.as_view(), name='evidence-list-create'),
    # Retrieve, update, and delete a specific Evidence
    path('evidence/<int:pk>/', EvidenceView.as_view(), name='evidence-list-create'),
    path('evidencebyincident/<uuid:incident_uuid>/', EvidenceByIncidentIdView.as_view(), name='evidence-by-incident'),
    # Retrieve, update, and delete a specific Incident
    path('complaint/<str:section_uuid>/', ComplaintView.as_view(), name='incident-detail'),
    # Retrieve all procedures associated with a specific Incident
    path('complaint/', ComplaintView.as_view(), name='incidents'),
    path('inspection-form/', InspectionFormView.as_view(), name='inspection-form-details'),
    path('inspection-form/<int:pk>/', InspectionFormView.as_view(), name='inspection-form-details-detail'),
    # path('incident/evidence/<int:evidence_id>/', IncidentByEvidenceAPIView.as_view(), name='incident_by_evidence_api'),
    path('inspection-labs-by-incident/<uuid:form_uuid>/', InspectionLabsByIncidentIdView.as_view(), name='inspection-labs-by-incident'),
    path('incident-statistics/', IncidentStatisticsView.as_view(), name='incident-statistics'),
    path('upload-images/', IncidentImageUploadView.as_view(), name='upload-incident-images'),
    path('upload-images/<str:insertUuid>/', IncidentImageUploadView.as_view(), name='list-incident-images'),
    path("sent-to-admin/", SentToAdminIncidentView.as_view()),
    path('sent-to-admin/<str:uuid>/', SentToAdminIncidentView.as_view(), name='incident-detail'),
]





