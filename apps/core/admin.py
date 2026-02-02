from django.contrib import admin
from django.utils.html import format_html, escape
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status_badge', 'created_at', 'action_buttons']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at', 'safe_message_preview']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'message', 'safe_message_preview')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def safe_message_preview(self, obj):
        """Display message with HTML escaped"""
        return format_html(
            '<div style="background: #f3f4f6; padding: 10px; border: 1px solid #d1d5db; max-height: 200px; overflow-y: auto;"><pre>{}</pre></div>',
            escape(obj.message)
        )
    safe_message_preview.short_description = 'Message Preview (Safe)'
    
    def status_badge(self, obj):
        colors = {
            'new': '#ef4444',
            'pending': '#f97316',
            'completed': '#22c55e',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def action_buttons(self, obj):
        if obj.status == 'new':
            return format_html(
                '<a class="button" href="mailto:{}">📧 Reply</a>',
                escape(obj.email)  # Escape email juga
            )
        return '-'
    action_buttons.short_description = 'Actions'
    
    actions = ['mark_as_pending', 'mark_as_completed']
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} message(s) marked as Pending.')
    mark_as_pending.short_description = 'Mark as Pending Response'
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} message(s) marked as Completed.')
    mark_as_completed.short_description = 'Mark as Completed'
