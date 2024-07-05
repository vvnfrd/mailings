from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from blogs.models import Blog
from django.views.generic.list import ListView


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_info.html'

    def get_object(self, queryset=None):
        self.blog = super().get_object(queryset)
        self.blog.views_counter += 1
        self.blog.save()
        return self.blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'text', 'image')
    success_url = reverse_lazy('blogs:blog_list')
    template_name = 'blog_form.html'


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'text', 'image')
    success_url = reverse_lazy('blogs:blog_list')
    template_name = 'blog_form.html'

    def get_success_url(self):
        return reverse('blogs:blog_info', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs:blog_list')
    template_name = 'blog_confirm_delete.html'
