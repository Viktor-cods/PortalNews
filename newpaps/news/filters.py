from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import *

class PostFilter(FilterSet):
    dateCreate = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label="Дата публикации до:",
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type' : 'datetime-local'},
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'postCategory': ['exact'],
        }