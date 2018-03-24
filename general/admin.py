# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'gmail', 'profile_image', 'role', 'bre_number', 'broker_license', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'bre_number', 'broker_license', 'role']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'lead', 'template', 'status', 'assign_to', 'created_by', 'created_at']
    search_fields = ['title']


class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'goal', 'created_by', 'created_at']
    search_fields = ['name']


class CircleAdmin(admin.ModelAdmin):
    list_display = ['name', 'goal', 'color', 'created_by', 'created_at']
    search_fields = ['name', 'goal']


class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address', 'address2', 'zipcode', 
    				'state', 'city', 'created_by', 'created_at']
    search_fields = ['first_name', 'last_name', 'address', 'address2','zipcode', 
    				 'state', 'city']


class EmailSettingAdmin(admin.ModelAdmin):
    list_display = ['subject', 'bcc', 'check_me', 'created_by', 'created_at']
    search_fields = ['subject', 'bcc']


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'email', 'share_circle', 'created_by', 'created_at']
    search_fields = ['name', 'color', 'email']


class CalendarPermissionAdmin(admin.ModelAdmin):
    list_display = ['team', 'calendar', 'can_view', 'can_modify']


admin.site.register(User, UserAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Event)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Circle, CircleAdmin)
admin.site.register(LeadCircle)
admin.site.register(Task, TaskAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Color)
admin.site.register(ProductOption)
admin.site.register(Interaction)
admin.site.register(LeadRelation)
admin.site.register(LeadFile)
admin.site.register(Notification)
admin.site.register(CalendarPermission, CalendarPermissionAdmin)
