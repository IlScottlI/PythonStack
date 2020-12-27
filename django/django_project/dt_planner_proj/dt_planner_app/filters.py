import django_filters
from dt_planner_app.models import Calendar


class CalendarFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    )

    ordering = django_filters.ChoiceFilter(
        label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Calendar
        fields = {
            'title': ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'created_at' if value == 'ascending' else '-created_at'
        return queryset.order_by(expression)
