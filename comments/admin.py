from django.contrib import admin

from .models import CommentsDb


@admin.register(CommentsDb)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('text', 'date', 'author', 'product', 'approved_comment')
    list_filter = ('approved_comment', 'date')
    search_fields = ('author', 'text')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved_comment=True)
