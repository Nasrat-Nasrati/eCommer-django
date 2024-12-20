from django.contrib import admin
from .models import Product,Variation ,ReviewRating,ProductGallery
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
     model = ProductGallery
     extra = 1

class productAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline]


class VaritionAdmin(admin.ModelAdmin):
     list_display = ('product','variation_category','variation_value','is_active')
     list_editable=('is_active',)
     list_filter = ('product','variation_category','variation_value')


admin.site.register(Product,productAdmin)
admin.site.register(Variation,VaritionAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)


