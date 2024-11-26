from typing import Any
from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode
from .models import Product, Collection, Customer, Order, OrderItem, Cart, CartItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory' # Parameter for the filter that will be used in the URL query.

    def lookups(self, request, model_admin):
        # a list of tuples
        return [
            ("<10", "Low")
        ]
    
    def queryset(self, request: Any, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ('title','unit_price','inventory', 'inventory_status','collection_title')
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )
    

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']
    list_per_page = 10

    def product_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id':str(collection.id)
            })) # link will be http://127.0.0.1:8000/admin/store/product/?collection__id=id'
        
        return format_html('<a href="{}">{}</a>', url, collection.product_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )
    
    

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'membership')
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ('id', 'placed_at', 'customer')
    list_select_related = ['customer']
 

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')