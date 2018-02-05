from django.contrib import admin
from .models import Post, Connection

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp']
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
admin.site.register(Connection)