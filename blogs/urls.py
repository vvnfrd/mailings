from django.urls import path, reverse_lazy
from django.views.decorators.cache import cache_page

from blogs.apps import BlogsConfig
from blogs.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogsConfig.name

urlpatterns = [
    path('blogs/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_info'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),

]
