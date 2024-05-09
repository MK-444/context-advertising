from django.contrib import admin
from .models import Tag, Advert


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tagname',)  


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_tag_names')  
    readonly_fields = ('get_tag_names',)  

    def get_tag_names(self, obj):
        return ", ".join([tag.tagname for tag in obj.tags.all()])  

    get_tag_names.short_description = 'Tags' 
