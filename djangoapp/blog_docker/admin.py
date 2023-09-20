from django.contrib import admin
from blog_docker.models import Tag, Category

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
    
@admin.register(Category)
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