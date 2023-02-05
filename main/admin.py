from pagedown.widgets import AdminPagedownWidget
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

admin.site.register(Comment)
admin.site.unregister(Group)



