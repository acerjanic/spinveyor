# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django import forms
from .models import Study, ReconProtocol


# Define admin views here
class StudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_recon_nf_file', 'created', 'modified' )
    prepopulated_fields = {'slug': ('name',)}

    def get_recon_nf_file(self, obj):
        return obj.recon_protocol.nf_file
    get_recon_nf_file.short_description = 'Recon Protocol NF File'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("Calling formfield_for_foreignkey in StudyAdmin")
        print(db_field)
        if db_field.name == 'recon_protocol':
            return ReconProtocolChoiceField(queryset=ReconProtocol.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ReconProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'nf_file', 'created', 'modified' )

class ReconProtocolChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

# Register your models here.
admin.site.register(Study, StudyAdmin)
admin.site.register(ReconProtocol, ReconProtocolAdmin)