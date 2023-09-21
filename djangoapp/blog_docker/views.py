from django.shortcuts import render
from django.core.paginator import Paginator
from blog_docker.models import Post
from django.db.models import Q # permite usar o pipe nas querys

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
        }
    )

def created_by(request, id):
    # filtra os posts pelo usuário que os criou
    posts = Post.objects.get_published().filter(created_by__pk=id)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def category(request, slug):
    # filtra os posts pela categoria
    posts = Post.objects.get_published().filter(category__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def tag(request, slug):
    # filtra os posts pela tag
    posts = Post.objects.get_published().filter(tags__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def tag(request, slug):
    # filtra os posts pela tag
    posts = Post.objects.get_published().filter(tags__slug=slug)
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
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
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'search_value': search_value
        }
    )

def page(request, slug):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page':
        }
    )

def post(request, slug):
    # pega um post expecífico
    post = Post.objects.get_published().filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
