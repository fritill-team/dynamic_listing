from django.urls import path

from blog.views import BlogTableView, UsersTableView, UserDetailView

app_name = 'blog'
urlpatterns = [
    path("blog/table/", BlogTableView.as_view(), name="blog-table"),

    path("users/table/", UsersTableView.as_view(), name="users-table"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-details"),

]
