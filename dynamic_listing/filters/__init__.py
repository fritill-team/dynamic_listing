from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .filter_field_renderer import *
from .filter_renderer import *
from .filters import *


class FilterSet(django_filters.FilterSet):
    filterset_types = {}
    fields_map = {
        "top_left": [],
        "top_right": [],
        "top_body": [],
        "side": []
    }
    force_visibility = []
    filterset_renderer = FilterRenderer

    RATE_CHOICES = (
        (4, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up")))),
        (3, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up")))),
        (2, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up")))),
        (1, mark_safe('<i class="text-warning fs-4 bi bi-star-fill"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '<i class="text-warning fs-4 bi bi-star"></i>'
                      '{}'.format(_(" & Up"))))
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applied_filters = []

        for name, filter_ in self.filters.items():
            value = self.data.get(name)

            if value:
                label = filter_.label
                key = name

                if isinstance(filter_, django_filters.MultipleChoiceFilter):
                    value = self.data.getlist(name)
                    for v in value:
                        value_label = self.get_value_label(filter_, v)
                        self.applied_filters.append(
                            {'label': label, 'key': key, 'value': v, 'value_label': value_label})
                else:
                    value_label = self.get_value_label(filter_, value)
                    self.applied_filters.append(
                        {'label': label, 'key': key, 'value': value, 'value_label': value_label})

    def get_value_label(self, filter_, value):
        if hasattr(filter_, 'field') and hasattr(filter_.field, 'choices'):
            value_label = None
            for k, v in filter_.field.choices:
                if str(k) == str(value):
                    value_label = v
                    break
        else:
            value_label = value

        return value_label

    def get_renderer(self):
        return self.filterset_renderer(self, self.get_filterset_types(), self.fields_map).as_fields()

    def get_filterset_types(self):
        return self.filterset_types

    def filter_boolean(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: value})
        return queryset

    def filter_rate(self, queryset, name, value):
        if not value:
            return queryset
        value = int(value)
        lookup = {}
        if value == 1:
            lookup = {name + "__lt": 2, name + "__gte": 1}
        elif value == 2:
            lookup = {name + "__lt": 3, name + "__gte": 2}
        elif value == 3:
            lookup = {name + "__lt": 4, name + "__gte": 3}
        elif value == 4:
            lookup = {name + "__lte": 5, name + "__gte": 4}

        return queryset.filter(**lookup)
