from django.contrib import admin

from . import models
from . import forms

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('drug', 'date_of_comming')
    list_display_links = ('drug',)
    # search_fields = ('title', 'text')
    form = forms.ShipmentForm
    # list_editable = ('is_published',)
    # list_filter = ('is_published', 'date', 'title')
    # prepopulated_fields = {"slug": ("title",)}
    admin_priority = 3

admin.site.register(models.Shipment, ShipmentAdmin)


class DrugAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    # search_fields = ('title', 'text')
    form = forms.DrugForm
    # list_editable = ('is_published',)
    # list_filter = ('is_published', 'date', 'title')
    # prepopulated_fields = {"slug": ("title",)}
    admin_priority = 1

admin.site.register(models.Drug, DrugAdmin)


class FirmAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    #search_fields = ('title', 'text')
    form = forms.FirmAdminForm
    #list_editable = ('is_published',)
    #list_filter = ('is_published', 'date', 'title')
    #prepopulated_fields = {"slug": ("title",)}
    admin_priority = 4

admin.site.register(models.Firm, FirmAdmin)


class DrugUnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    # search_fields = ('title', 'text')
    form = forms.DrugUnitForm
    #list_editable = ('is_published',)
    #list_filter = ('is_published', 'date', 'title')
    #prepopulated_fields = {"slug": ("title",)}
    admin_priority = 2

admin.site.register(models.DrugUnit, DrugUnitAdmin)

class MovementAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'department', 'amount')
    list_display_links = ('shipment',)
    #search_fields = ('title', 'text')
    form = forms.MovementForm
    #list_editable = ('is_published',)
    #list_filter = ('is_published', 'date', 'title')
    #prepopulated_fields = {"slug": ("title",)}
    admin_priority = 5

admin.site.register(models.Movement, MovementAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    #search_fields = ('title', 'text')
    form = forms.DepartmentForm
    #list_editable = ('is_published',)
    #list_filter = ('is_published', 'date', 'title')
    #prepopulated_fields = {"slug": ("title",)}
    admin_priority = 6

admin.site.register(models.Department, DepartmentAdmin)


from django.apps import apps
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    from django.contrib.admin.sites import site
    for app_name in app_dict.keys():
        app = app_dict[app_name]
        model_priority = {
            model['object_name']: getattr(
                site._registry[apps.get_model(app_name, model['object_name'])],
                'admin_priority',
                20
            )
            for model in app['models']
        }
        app['models'].sort(key=lambda x: model_priority[x['object_name']])
        yield app

admin.AdminSite.get_app_list = get_app_list