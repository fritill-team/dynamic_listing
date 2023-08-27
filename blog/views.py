from django.contrib.auth.models import User
from django.views.generic import DetailView

from blog.filters import BlogsFilter
from blog.models import Blog
from dynamic_listing.views import DynamicTableView, dynamic_table_factory


class BlogTableView(DynamicTableView):
    model = Blog
    title = "Blogs"
    filterset_class = BlogsFilter
    row_template_name = 'blog/table/_table_row.html'
    load_rows_from_template = True
    table_columns = (
        ('id', "ID"),
        ('title', "Title", "text-start max-w-200px"),
        ('content', "Content", "text-center max-w-200px"),
        ('category', "Category", "text-center"),
        ('tags', "Tags", "text-center"),
    )

    def get_breadcrumb(self):
        return [
            {"title": "Home", "url": '/'},
            {"title": "Blogs"},
            {"title": "Table"}
        ]


BlogTablefactory = dynamic_table_factory(
    model=Blog,
    load_rows_from_template=True,
    filterset_class=BlogsFilter,
    row_template_name='blog/table/_table_row.html',
    table_columns=(
        ('id', "ID"),
        ('title', "Title", "text-start max-w-200px"),
        ('content', "Content", "text-center max-w-200px"),
        ('category', "Category", "text-center"),
        ('tags', "Tags", "text-center"),
    )
)


class UsersTableView(DynamicTableView):
    model = User
    title = "Users"
    row_template_name = 'users/table/_table_row.html'
    load_rows_from_template = True
    table_columns = (
        ('id', "ID"),
        ('full_name', "Fullname", "text-start"),
        ('email', "Email", "text-center"),
        ('is_active', "Active", "text-center"),
        ('date_joined', "Date Joined", "text-center"),
    )


class UserDetailView(DetailView):
    model = User
    template_name = 'users/details/index.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.get_full_name
        context['blogs'] = BlogTablefactory(self.request, queryset=self.object.blog_set.all())
        return context
