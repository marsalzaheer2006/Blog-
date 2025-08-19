from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Tweet, BlogPost, ContactMessage

# Custom Admin Site that only allows superusers
class SuperUserAdminSite(AdminSite):
    site_header = "Arsal's Blog - Super Admin"
    site_title = "Arsal's Blog Admin"
    index_title = "Welcome to Arsal's Blog Administration"
    
    def has_permission(self, request):
        """
        Only allow superusers to access the admin panel
        """
        return request.user.is_active and request.user.is_superuser
    
    def login(self, request, extra_context=None):
        """
        Custom login that checks for superuser status
        """
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                messages.error(request, 'Access denied. Only the main administrator can access this area.')
                return HttpResponseRedirect(reverse('home'))
        return super().login(request, extra_context)

# Create custom admin site instance
admin_site = SuperUserAdminSite(name='superuser_admin')

@admin.register(BlogPost, site=admin_site)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('author', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

# Register models with the custom admin site
admin_site.register(Tweet)
admin_site.register(ContactMessage)
admin_site.register(User)
admin_site.register(Group)

# Keep the default admin site but unregister all models from it
try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass
