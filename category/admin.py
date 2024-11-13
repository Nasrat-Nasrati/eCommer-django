from django.contrib import admin

# Register your models here.
from .models import category

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug': ('category_name',)}
    list_display =('category_name','slug')

admin.site.register(category,categoryAdmin)

