from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View


def content(request):
    return render(request, 'flatpages/main.html')


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'news_list'
    queryset = Post.objects.filter(type=True)
    template_name = 'news_list.html'


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class ArticlesDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news.html'
    queryset = Post.objects.filter(type=True)
    context_object_name = 'news'


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = True
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class NewsSearch(NewsList):
    template_name = 'news_search.html'

# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
#         return context

# class MyView(PermissionRequiredMixin, View):
#     permission_required = ('<app>.<action>_<model>',
#                            '<app>.<action>_<model>')