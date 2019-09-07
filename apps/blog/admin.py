from django.contrib import admin
from apps.blog.models import Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "modified", "publish")
    list_per_page = 20


admin.site.register(Post, PostAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_per_page = 20


admin.site.register(Like, LikeAdmin)
