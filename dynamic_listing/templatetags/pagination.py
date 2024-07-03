from django import template

register = template.Library()


@register.simple_tag
def get_paginated_range(paginator, current_page):
    return paginator.get_elided_page_range(current_page,  on_each_side=2, on_ends=2)
