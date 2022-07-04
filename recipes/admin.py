from django.contrib import admin

from .models import Category, Recipe


# Register your models here.
class CategoryaAdmin(admin.ModelAdmin):
    ...


class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryaAdmin)
admin.site.register(Recipe, RecipeAdmin)
