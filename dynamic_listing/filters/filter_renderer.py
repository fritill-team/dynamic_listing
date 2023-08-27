from .filter_field_renderer import FIELD_RENDERER_MAP


class FilterRenderer:
    def __init__(self, filterset, filterset_types, fields_map):
        self.filters = {
            "top_left": [],
            "top_right": [],
            "top_body": [],
            "side": []
        }
        self.filterset = filterset
        self.filterset_types = filterset_types
        self.fields_map = fields_map

    def as_fields(self):
        for name, filter_field in self.filterset.filters.items():

            value = self.filterset.form.data.get('name', None)
            renderer = self.get_filter_renderer_field(filter_field)
            try:
                filter_renderer = renderer(
                    filter_field=filter_field,
                    form_field=self.filterset.form[name],
                    value=value,
                    filter_type=self.filterset_types.get(name) if self.filterset_types.get(name, None) else 'filter',
                )
                if not filter_renderer.is_hidden() or name in self.filterset.force_visibility:
                    position = self.get_position(name)
                    self.filters[position].append(filter_renderer.get())

            except Exception as e:
                raise Exception("No Renderer Implemented for: \"{}\"".format(type(filter_field)))

        return self.filters

    def get_filter_renderer_field(self, filter_field):
        return FIELD_RENDERER_MAP.get(type(filter_field))

    def get_position(self, name):
        for position, fields in self.fields_map.items():
            if name in fields:
                return position
        return "side"
