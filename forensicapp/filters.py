import django_filters
from .models import *
class IncidentFilter(django_filters.FilterSet):
    # Text field filters
    date_discovery = django_filters.CharFilter(lookup_expr='icontains')
    action_taken = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date filtering (based on actual model field accident_date which is a TextField)
    # If `accident_date` is truly a string field, this filter may not work properly.
    # Consider converting it to DateField in the model for proper date filtering.
    incident_date_range = django_filters.DateFromToRangeFilter(field_name="accident_date")

    # Category and type
    category_accident = django_filters.ChoiceFilter(choices=Incident._meta.get_field('category_accident').choices)
    typeAccident = django_filters.CharFilter(lookup_expr='icontains')

    # City filter
    accident_city = django_filters.CharFilter(lookup_expr='icontains')

    # Location & status
    accident_location = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='icontains')

    # User filter
    user = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.all(), null_label="Any User")

    # Optional investigation filters
    investigating_body = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Incident
        fields = [
            'date_discovery', 'action_taken',
            'incident_date_range',
            'category_accident', 'typeAccident',
            'accident_city', 'accident_location',
            'color', 'investigating_body', 'user',
        ]

class InspectionFilter(django_filters.FilterSet):
    #  filters 
    request_authority=django_filters.CharFilter(lookup_expr='icontains')
    incident =django_filters.CharFilter(lookup_expr='icontains')
    inspection_date = django_filters.DateFilter(field_name='inspection_date')
    inspection_date_range = django_filters.DateFromToRangeFilter(field_name="inspection_date")



    class Meta:
        model = InspectionForm
        fields = ['request_authority' , 'inspection_date' , 'incident' , 'inspection_date_range']

