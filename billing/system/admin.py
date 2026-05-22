from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.html import format_html


@admin.register(CustomerInformation)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('select_customer','gst_number','email','address')
    list_filter = ('select_customer','gst_number','email','address')
    search_fields = ('select_customer','gst_number','email','address')
    ordering = ('-id',)

    fields=('select_customer','gst_number','email','address')
    readonly_fields = ('gst_number',)

@admin.register(JobNumber)
class JobNumberAdmin(admin.ModelAdmin):
    list_display = ('job_number', 'date', 'duedate', 'descriptions')
    list_filter = ('job_number','date', 'duedate','descriptions')
    search_fields = ('job_number','date','duedate','descriptions')
    ordering = ('-id',)

    fieldsets = (
        ('Job Number', {'fields': ('job_number',)}),
        ('Date', {'fields': ('date',)}),
        ('Due Date', {'fields': ('duedate',)}),
        ('Description', {'fields': ('descriptions',)}),
    )
    readonly_fields = ('job_number',)
    
@admin.register(JobItems)
class JobItemsAdmin(admin.ModelAdmin):
    list_display = ('material','length','width','quantity','area','anodising_type','thickness','color_finish','process_charges')
    list_filter = ('material', 'area','anodising_type','thickness','color_finish','process_charges')
    search_fields = ('material','length','width','quantity','area','anodising_type','thickness','color_finish','process_charges')
    ordering = ('-id',)

    fieldsets = (
        ('material', {'fields': ('material',)}),
        ('length', {'fields': ('length',)}),
        ('width', {'fields': ('width',)}),
        ('quantity', {'fields': ('quantity',)}),
        ('area', {'fields': ('area',)}),
        ('anodising_type', {'fields': ('anodising_type',)}),
        ('thickness', {'fields': ('thickness',)}),
        ('color_finish', {'fields': ('color_finish',)}),
        ('process_charges', {'fields': ('process_charges',)}),
    )