from django.shortcuts import render
from django.core.paginator import Paginator
from blog_docker.models import Post

# Create your views here.

PER_PAGE = 9

def index(request):
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

def page(request, slug):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page':
        }
    )

def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
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