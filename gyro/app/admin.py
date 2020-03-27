# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django import forms
from .models import Study, ReconProtocol, Recon, ResultFile, ReconLogFile


# Define admin views here
class StudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_recon_nf_file', 'created', 'modified' )
    prepopulated_fields = {'slug': ('name',)}

    def get_recon_nf_file(self, obj):
        return obj.recon_protocol.nf_file
    get_recon_nf_file.short_description = 'Recon Protocol NF File'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'recon_protocol':
            return ReconProtocolChoiceField(queryset=ReconProtocol.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ReconProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'nf_file', 'created', 'modified' )


class ReconProtocolChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class StudyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ReconAdmin(admin.ModelAdmin):
    list_display = ('id', 'study', 'subject_id', 'created_at', 'created_by')
    exclude = ['created_by',]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'study':
            return StudyChoiceField(queryset=Study.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'study', 'subject_id', 'created_at', 'created_by']
        else:
            return []


class ResultFileAdmin(admin.ModelAdmin):
    list_display = ('recon_id', 'url', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ReconLogFileAdmin(admin.ModelAdmin):
    list_display = ('recon_id', 'url', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Study, StudyAdmin)
admin.site.register(ReconProtocol, ReconProtocolAdmin)
admin.site.register(Recon, ReconAdmin)
admin.site.register(ResultFile, ResultFileAdmin)
admin.site.register(ReconLogFile, ReconLogFileAdmin)