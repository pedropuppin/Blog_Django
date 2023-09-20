from django.contrib import admin
from django.http.request import HttpRequest
from site_setup.models import MenuLink, SiteSetup

# Register your models here.

# o registro dos links pode ficar comentado pq com o inline não temos mais a
# necessidade de mostrar ele no /admin
# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path',
#     list_display_links = 'id', 'text', 'url_or_path',
#     search_fields = 'id', 'text', 'url_or_path',
    

# permite mostrar e criar um link dentro do setupAdmin
class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1
    
    
@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = MenuLinkInline,

    # remove a possibilidade de criar mais de um setup
    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()