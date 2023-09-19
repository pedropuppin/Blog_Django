from django.urls import path
from blog_docker.views import index

app_name = 'blog'

urlpatterns = [
    path('', index, name = 'index'),
]

