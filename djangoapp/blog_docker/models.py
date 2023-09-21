from django.db import models
from utils.rand_slug import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment # type: ignore
from django.urls import reverse

# Create your models here.

class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


#####################################################################

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=100,
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
##################################################################### 
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
#####################################################################

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )
    is_published = models.BooleanField(
        default=False,
        help_text='Este campo precisará estar marcado para a página ser exibida publicamente.'
    )
    content = models.TextField()
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:page', args=(self.slug,))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    
#####################################################################

class PostManager(models.Manager): # é uma forma de evitar repetição de cod
    def get_published(self): # o self aqui é o objects da classe Post
        return self.filter(is_published=True).order_by('-pk')

#####################################################################

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    # objects = models.Manager // manager padrão que pode ser extendido PostManager
    objects = PostManager()
      
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text='Este campo precisará estar marcado para o post ser exibido publicamente.'
    )
    content = models.TextField()
    
    cover = models.ImageField(
        upload_to='posts/%Y/%m/',
        blank=True,
        default='',
    )
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Se marcado exibirá a capa dentro do post'
    )
    
    # auto_now_add adiciona a data em que o post foi salvo e é isso
    created_at = models.DateTimeField(auto_now_add=True)
    
    # related name subistitui o user.post_set.all() por user.post_created_by.all()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    
    # auto_now toda vez que salvar vai gerar uma nova data
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    
    # um post pertence a uma categoria
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    
    # um post tem muitas tags e uma tag muitos posts 
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        default=''
    )
    
    # Método que cria um link absoluto. Faz aparecer um 'ver no site' lá no admin
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        
        return reverse('blog:post', args=(self.slug,))
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False
  
        # se o cover for diferente do current muda pra True
        if self.cover:
            cover_changed = current_cover_name != self.cover.name
            
        # se for True redimenciona a imagem
        if cover_changed:
            resize_image(self.cover, 900)
            
        return super_save
    
    def __str__(self) -> str:
        return self.title