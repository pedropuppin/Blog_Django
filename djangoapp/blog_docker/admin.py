from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog_docker.models import Tag, Category, Page, Post

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug'
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    
    # diz que o campo de slug vai ser pre populado com o valor do campo de name 
    prepopulated_fields = {
        "slug": ('name',),
    }
    
#####################################################################

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug'
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id', 
    prepopulated_fields = {
        "slug": ('name',),
    }
    
#####################################################################
    
@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published'
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }
    
#####################################################################
    
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published', 'created_by'
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'excerpt' ,'content', 'cover'
    list_per_page = 50
    list_filter = 'is_published', 'category'
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by'
    prepopulated_fields = {
        "slug": ('title',),
    }
    autocomplete_fields = 'tag', 'category'
    
    # permite salvar o created_by e o updated_by user de cada post
    # esse save só funciona na parte administrativa do post    
    def save_admin(self, request, obj, form, change):
        # o 'change' permite saber se a gente tá criando ou alterando
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
            