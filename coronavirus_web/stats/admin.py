from django.contrib import admin
from django.http import HttpResponseRedirect

# Register your models here.
from .models import *


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'region',)
    list_display_links = ('id', 'region',)
    search_fields = ('id', 'region', )


class RegionalStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'region', 'new_cases', 'collective_immunity',)
    search_fields = ('id', 'date', 'region',)


class RegionalRestrictionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'region', 'restriction',)
    search_fields = ('id', 'region', 'restriction', )


class RestrictionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('description', )


class LastParsedAdmin(admin.ModelAdmin):
    change_list_template = "admin/parsed_change_list.html"
    list_display = ('parse_datetime', 'parsed_info_datetime',)


admin.site.register(Regions, RegionsAdmin)
admin.site.register(RegionalStats, RegionalStatsAdmin)
admin.site.register(RegionalRestrictions, RegionalRestrictionsAdmin)
admin.site.register(Restrictions, RestrictionsAdmin)
admin.site.register(LastParsed, LastParsedAdmin)
