from django.contrib import admin
from .models import Board, Comment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):  # admin.ModelAdmin을 상속하겠다.
    list_display = ('title', 'content', 'created_at', 'updated_at', )
    readonly_fields = ['created_at', 'updated_at', ]
    # readonly_fields


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('content', )