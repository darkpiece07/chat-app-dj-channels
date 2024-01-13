from django.contrib import admin
from .models import Group, Chat
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ['content', 'timestamp', 'group']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Group)
admin.site.register(Chat, ChatAdmin)

