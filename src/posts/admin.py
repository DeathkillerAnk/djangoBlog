# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.contrib import admin

from .models import Post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","content","timestamp","updated"]
    list_display_links = ["title"]
    list_filter = ["timestamp","updated"]
    search_fields = ["title","content"]
   # list_editable = ["content"]
    class Meta:
        model = Post
admin.site.register(Post,PostModelAdmin)
