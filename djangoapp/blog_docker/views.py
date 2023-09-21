from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from blog_docker.models import Post, Page, Tag
from django.db.models import Q # permite usar o pipe nas querys
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

# Create your views here.

PER_PAGE = 9

class PostListView(ListView):
    # precisa informar qual o model, o nome do template e o objeto que vai ser renderixado
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() # pega todos os posts tira a necessidade de info o model

    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - ',
        })
        
        return context
    

class CreatedByListView(PostListView):
    # contexto temporário
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
            
        page_title = 'Posts de ' + user_full_name + ' - '
        
        context.update({
            'page_title': page_title,
        })
    
        return context
    
    # filtra os posts pelo usuário que os criou
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs
    
    def get(self, request, *args, **kwargs):
        # self.kwargs.get('id') -> traz o id argumento da url
        user_id = self.kwargs.get('id')
        user = User.objects.filter(pk=user_id).first()
        
        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'user_id': user_id,
            'user': user
        })
        
        return super().get(request, *args, **kwargs)
    

class CategoryListView(PostListView):
    allow_empty = False
    # substitui 
    # if len(page_obj) == 0:
    #   raise Http404
    
    # filtra os posts pela categoria
    def get_queryset(self):
        return super().get_queryset().filter(
            # self.kwargs.get('slug') -> traz o argumento da url
            category__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)
        page_title = f'Categoria - {self.object_list[0].category.name} - '
        # self.object_list pega toda a lista de objetos
        
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx
    
    
class TagListView(PostListView):
    allow_empty = False
    
    # filtra os posts pela tag
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('slug')
        tag = Tag.objects.get(slug=tag_slug)
        page_title = (
            f'Tag - {tag.name} - '   
        )
        
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx
    
    
class SearchListView(PostListView):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._search_value = ''
        
    #pega o valor de search do formulário
    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    # filtra os posts pelo valor da busca
    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'Search - {search_value[:30]} - ',
            'search_value': search_value,
        })
        return ctx
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'Página - {page.title} - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    # slug_field = 'slug' // é padrão poderia ser ignorado
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'Post - {post.title} - '
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)
    
