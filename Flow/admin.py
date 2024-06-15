# In your admin.py file

from django.contrib import admin

from .models import Flow


# Custom action to mark selected flows as active
def mark_as_active(modeladmin, request, queryset):
    # Update the following line according to your model's fields
    queryset.update(status='active')  # Assuming 'status' field exists in Flow
    modeladmin.message_user(request, "Selected flows have been marked as active.")


mark_as_active.short_description = "Mark selected flows as active"


# Define the FlowAdmin class
class FlowAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'teacher')
    list_filter = ('subject', 'teacher')
    search_fields = ('name',)
    actions = [mark_as_active]


# Register the Flow model with the FlowAdmin class
admin.site.register(Flow, FlowAdmin)
