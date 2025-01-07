from django.contrib import admin
from .models import Character
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.

class CharacterResource(resources.ModelResource):

    class Meta:
        model = Character

@admin.register(Character)
class CharacterAdmin(ImportExportActionModelAdmin):
    resource_classes = [CharacterResource]