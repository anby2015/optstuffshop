# -*- coding: utf-8 -*-
from django.contrib import admin
from catalog.models import *
from mpttadmin import MpttAdmin
from tinymce.widgets import TinyMCE
from django.db import models
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage
from sorl.thumbnail.admin import AdminImageMixin, AdminImageWidget



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formfield_overrides = {
        models.ImageField: {
            'widget': AdminImageWidget,
        }
    }

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('title','menu_node_id','price')
    list_editable = ('price',)
    radio_fields = {"num_of_sim": admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': ('title', 'menu_node_id', 'price', 'description')
        }),
        ('Параметры', {
            'fields': ('num_of_sim','is_special', 'has_wifi', 'has_bluetooth', 'has_gps', 'has_tv','features')
        }),
    )
    inlines = [
        ProductImageInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 50})},
    }
admin.site.register(Phone,PhoneAdmin)


class ProductImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'product_id', 'image',)
    list_filter = ('product_id',)
    formfield_overrides = {
        models.ImageField: {
            'widget': AdminImageWidget,
        }
    }
admin.site.register(ProductImage, ProductImageAdmin)


class MenuNodeAdmin(MpttAdmin):
    tree_title_field = 'name'
    tree_display = ('name','get_absolute_url')

    class Meta:
        model = MenuNode
admin.site.register(MenuNode, MenuNodeAdmin)



class FlatPageAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 50})},
        }
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
