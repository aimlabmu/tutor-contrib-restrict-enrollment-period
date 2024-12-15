from django.contrib import admin
from .models import CourseEnrollmentRule


@admin.register(CourseEnrollmentRule)
class CourseEnrollmentRuleAdmin(admin.ModelAdmin):
    list_display = ('course', 'min_days_before_access', 'max_days_until_expiry', 'updated_at')
    list_filter = ('min_days_before_access', 'max_days_until_expiry')
    search_fields = ('course__display_name', 'course__id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('course',)
        }),
        ('Access Rules', {
            'fields': ('min_days_before_access', 'max_days_until_expiry')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
