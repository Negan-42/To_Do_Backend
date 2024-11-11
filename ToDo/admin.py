#admin.py
from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'complete', 'created')  # Fields to show in the admin list
    list_filter = ('complete', 'user')  # Filters in the admin sidebar
    search_fields = ('title', 'description')  # Enable search by title or description
    ordering = ('-created',)  # Order by created date, most recent first
    date_hierarchy = 'created'  # Adds a date-based drilldown navigation
    list_editable = ('complete',)  # Allows editing 'complete' status directly in the list view
    list_per_page = 25  # Pagination to show 25 tasks per page

    # Optionally, you can customize how the form looks in the admin
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'complete')
        }),
        ('Date Information', {
            'fields': ('created',),
            'classes': ('collapse',),  # Make this section collapsible
        }),
    )

    # Making 'created' field read-only (since it's auto-generated)
    readonly_fields = ('created',)
