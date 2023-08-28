import random
import string

from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.views.generic.list import MultipleObjectMixin


class DynamicListInit:
    def __init__(self, request=None, queryset=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.queryset = queryset
        self.request = request
        self.object_list = self.get_queryset()


class BulkActionsMixin:
    bulk_actions = None

    def get_bulk_actions(self):
        return self.bulk_actions

    def get_context_data(self, *args, **kwargs):
        context = super(BulkActionsMixin, self).get_context_data(*args, **kwargs)
        context['bulk_actions'] = self.get_bulk_actions()
        return context


class MediaMixin:
    def __init__(self, *args, **kwargs):
        self.media = {"css": [], 'js': []}

        super(MediaMixin, self).__init__(*args, **kwargs)

    def get_media(self):
        return mark_safe(self.get_js() + self.get_css())

    def get_js(self):
        self.media['js'].append('dynamic_listing/dynamic_listing.js')

        js = ''

        if 'js' not in self.media:
            return js

        for item in self.media['js']:
            js += '<script src="{}"></script>'.format(static(item))

        return js

    def get_css(self):
        css = ''
        if 'css' not in self.media:
            return css

        for item in self.media['css']:
            css += '<link href="{}">'.format(static(item))
        return css

    def get_context_data(self, *args, **kwargs):
        context = super(MediaMixin, self).get_context_data(*args, **kwargs)
        context['media'] = self.get_media()
        return context


class FilterMixin:
    filterset_class = None

    def __init__(self, *args, **kwargs):
        self.filterset_renderer = None
        self.applied_filters = []

        super(FilterMixin, self).__init__(*args, **kwargs)

    def check_filterset_class(self):
        filterset_class = self.get_filterset_class()
        return filterset_class and hasattr(filterset_class, 'filterset_renderer')

    def get_filterset_class(self):
        return self.filterset_class

    def get_filter(self, queryset):
        if self.check_filterset_class():
            filters = self.get_filterset_class()(self.request.GET, queryset)
            return filters, filters.get_renderer, filters.applied_filters
        return None, None, []

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        context['filter'] = self.filterset_renderer
        context['applied_filters'] = self.applied_filters
        return context


class BaseList(BulkActionsMixin, MediaMixin, FilterMixin, MultipleObjectMixin):
    queryset = None
    request = None
    listing_type = ''
    model = None
    paginate_by = 10
    listing_actions = None
    modals_template_name = None
    load_actions_from_template = False
    header_template_name = None
    factory = False
    container_class = "app-container container-xxl"

    def __init__(self, *args, **kwargs):
        source = string.ascii_letters + string.digits
        self.id = ''.join((random.choice(source) for i in range(8)))
        self.applied_filters = []
        if self.extra_context is None:
            self.extra_context = {}

        super(BaseList, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.render()

    def render(self):
        return mark_safe(render_to_string('dynamic_listing/partials/_listing_inner.html', self.get_context_data()))

    def get_queryset(self):
        queryset = super(BaseList, self).get_queryset()
        if self.check_filterset_class():
            filters, self.filterset_renderer, self.applied_filters = self.get_filter(queryset)
            queryset = filters.qs
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(BaseList, self).get_context_data(*args, **kwargs)
        context['request'] = self.request
        context['list_id'] = self.id
        context['actions'] = self.get_listing_actions()
        context['listing_type'] = self.listing_type
        context['factory'] = self.factory
        context['container_class'] = self.container_class
        if self.modals_template_name:
            context['modals_template_name'] = self.modals_template_name
        if self.header_template_name:
            context['header_template_name'] = self.header_template_name
        return context

    def get_listing_actions(self):
        return self.listing_actions


class DynamicTable(BaseList):
    listing_type = 'table'
    table_columns = ()
    load_rows_from_template = False
    row_template_name = None
    actions_template_name = None

    def get_context_data(self, *args, **kwargs):
        context = super(DynamicTable, self).get_context_data(*args, **kwargs)
        context['columns'] = self.process_table_columns()
        context['load_rows_from_template'] = self.load_rows_from_template
        if self.load_rows_from_template:
            context['row_template_name'] = self.row_template_name
        else:
            context['rows'] = self.load(context['object_list'])

        if self.load_actions_from_template:
            context['actions_template_name'] = self.actions_template_name

        return context

    def load(self, object_list):
        items = []
        for item in object_list:
            items.append(self._load_object_row(item))
        return items

    def _load_object_row(self, obj):
        row = []
        for column_name, text in self.get_table_columns():
            method = "load_{}".format(column_name)
            if hasattr(self, method) and callable(getattr(self, method)):
                call = getattr(self, method)
                row.append(call(obj))
            else:
                row.append(mark_safe('<td>{}</td>'.format(getattr(obj, column_name))))
        return row

    def process_table_columns(self):
        columns = []
        for column in self.get_table_columns():
            columns.append((column[0], column[1], column[2] if len(column) > 2 else ''))
        return columns

    def get_table_columns(self):
        return self.table_columns


class DynamicGrid(BaseList):
    listing_type = 'grid'
    item_template_name = None

    def get_context_data(self, *args, **kwargs):
        context = super(DynamicGrid, self).get_context_data(*args, **kwargs)
        context['item_template_name'] = self.item_template_name
        return context


class DynamicList(DynamicGrid):
    listing_type = 'list'
