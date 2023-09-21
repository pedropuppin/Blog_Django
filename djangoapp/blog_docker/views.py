from django.shortcuts import render
from django.core.paginator import Paginator
from blog_docker.models import Post, Page
from django.db.models import Q # permite usar o pipe nas querys
from django.contrib.auth.models import User
from django.http import Http404

# Create your views here.

PER_PAGE = 9

def index(request):
    # pega todos os posts
    posts = Post.objects.get_published()
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'Home - ',
        }
    )

def created_by(request, id):
    # filtra os posts pelo usuário que os criou
    posts = Post.objects.get_published().filter(created_by__pk=id)
    
    user = User.objects.filter(pk=id).first()
    if user is None:
        raise Http404()
    
    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'
        
    page_title = 'Posts de ' + user_full_name + ' - '
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,

        }
    )

def category(request, slug):
    # filtra os posts pela categoria
    posts = Post.objects.get_published().filter(category__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0:
        raise Http404
    
    page_title = f'Categoria - {page_obj[0].category.name} - '
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def tag(request, slug):
    # filtra os posts pela tag
    posts = Post.objects.get_published().filter(tags__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0:
        raise Http404
 
    page_title = f'Tag - {page_obj[0].tags.first().name} - '
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def search(request):
    #pega o valor de search do formulário
    search_value = request.GET.get('search', '').strip()
    
    # filtra os posts pelo valor da busca
    posts = (
        Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )
    )
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    page_title = f'Search - {search_value[:30]} - '
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'search_value': search_value,
            'page_title': page_title,
        }
    )

def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()
    
    if page_obj is None:
        raise Http404
 
    page_title = f'Página - {page_obj.title} - '
    
    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )

def post(request, slug):
    # pega um post expecífico
    post_obj = Post.objects.get_published().filter(slug=slug).first()
    
    if post_obj is None:
        raise Http404
 
    page_title = f'Post - {post_obj.title} - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
