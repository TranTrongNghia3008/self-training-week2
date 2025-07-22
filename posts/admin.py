from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django import forms
from .models import Post, Comment

@admin.action(description="Mark selected posts as Published")
def publish_posts(modeladmin, request, queryset):
    queryset.update(status='published')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at',         'short_description', 'view_comments_link')
    list_filter = ('status', 'author', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = [publish_posts]

    fieldsets = (
        ("Post Content", {
            "fields": ('title', 'content')
        }),
        ("Author & Status", {
            "fields": ('author', 'status'),
            "classes": ('collapse',),
        }),
    )

    def short_description(self, obj):
        description = obj.content[:10] + '...' if len(obj.content) > 10 else obj.content
        return format_html('<span title="{}"><i>{}</i></span>', obj.content, description)   

    short_description.short_description = 'Short Description'

    def view_comments_link(self, obj):
        count = obj.comments.count()
        url = (
            reverse('admin:posts_comment_changelist')
            + '?'
            + urlencode({'post__id': obj.id})
        )
        return format_html('<a href="{}">Comments ({})</a>', url, count)        
    view_comments_link.short_description = 'View Comments'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs.update({'placeholder': 'Enter post title'})
        form.base_fields['title'].label = 'Post Title'
        return form

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'content')
    ordering = ('-created_at',)

    fieldsets = (
        ("Comment Details", {
            "fields": ('post', 'author', 'content')
        }),
    )