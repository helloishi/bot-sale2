from django.utils import timezone
from django_filters import rest_framework as filters
from .models import Discount

class DiscountFilter(filters.FilterSet):
    class Meta:
        model = Discount
        fields = []

    def filter_queryset(self, queryset):
        today = timezone.now().date()
        return queryset.filter(start_date__lte=today, end_date__gte=today)
