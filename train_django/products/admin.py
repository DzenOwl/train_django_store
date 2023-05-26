from django.contrib import admin

from products.models import BasketItem, Product, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(BasketItem)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', 'short_description', ('price', 'quantity'), 'category')
    # readonly_fields = ('price', 'quantity', 'category')
    ordering = ('name',)
    search_fields = ('name',)


class BasketItemAdminInline(admin.TabularInline):
    model = BasketItem
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp', 'product')
    extra = 0
