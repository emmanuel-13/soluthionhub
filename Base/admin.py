from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class RoomInline(admin.StackedInline):
    model = Room
    extra = 1



@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['updated', 'created']
    inlines = [RoomInline]

# admin.site.register(Topic)
# admin.site.register(Room)
class MessageInline(admin.StackedInline):
    model = Message 
    extra = 1




@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['host', 'topic', 'name', 'description']
    list_filter = ['updated', 'created', 'host', 'topic']
    search_fields = ['host', 'topic', 'name'] 
    fieldsets = (
        ('Host and Topic', {
            "fields": ('host', 'topic',),
        }), 
        ('Room Details', {
            'fields': ('name', 'description', 'participants')
        }),
    )
    inlines = [MessageInline]

admin.site.register(Message)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'avatar']
    list_display_links = ['email']
    list_editable = ['username']
    exclude = ['password']
    search_fields = ['username', 'email']
