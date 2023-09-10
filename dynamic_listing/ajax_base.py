from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View


class Datatable:
    def __init__(self, model=None):
        self.columns = []
        self.model = model

    def column(self, name, label, ordarable=True, searchable=True, class_name=None):
        data = name
        self.columns.append({
            "data": data,
            "name": name,
            "title": label,
            "orderable": ordarable,
            "searchable": searchable,
            "class_name": class_name,
        })


class HyperListingBase:
    LISTING_TYPE_TABLE = 'table'
    LISTING_TYPE_GRID = 'grid'
    LISTING_TYPE_LIST = 'list'
    LISTING_TYPES = (
        (LISTING_TYPE_TABLE, _('Table')),
        (LISTING_TYPE_GRID, _('Grid')),
        (LISTING_TYPE_LIST, _('List')),
    )

    listing_type = 'table'
    config = {}

    def __init__(self, *args, **kwargs):
        if self.extra_context is None:
            self.extra_context = {}
        super(HyperListingBase, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['listing_type'] = self.listing_type
        context['listing_types'] = self.LISTING_TYPES
        return context

    def get_config(self):
        return self.config


class HyperListingView(View):
    listing_class = None

    def get(self, request, *args, **kwargs):
        hyper_listing = self.listing_class()

        return render(request, 'hyper_listing/index.html', {

        })
