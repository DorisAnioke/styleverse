from django.contrib import admin
from .models import (
    Category, Size, Color, Product, ProductImage,
    Order, OrderItem, Review, Wishlist, OrderTracking
)
from django.core.mail import send_mail
from .utils import send_tracking_update_email
from .models import HeroImage  

# --- CATEGORY ADMIN ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# --- SIZE ADMIN ---
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)


# --- COLOR ADMIN ---
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


# --- PRODUCT IMAGE INLINE ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# --- PRODUCT ADMIN ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category', 'sizes', 'colors')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
    filter_horizontal = ('sizes', 'colors')


# --- ORDER ITEM INLINE ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# --- ORDER ADMIN ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


# --- ORDER ITEM ADMIN ---
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


# --- REVIEW ADMIN ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name')


# --- WISHLIST ADMIN ---
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('products',)


# --- ORDER TRACKING ADMIN ---
@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'location', 'updated_at']
    list_filter = ['status', 'updated_at']
    search_fields = ['order__id', 'status', 'location']
    readonly_fields= ['updated_at']
    ordering = ['-updated_at']
    
    def save_model(self, request, obj, form, change):
        """
        When an OrderTracking object is saved via the admin, send an email notification.
        
        """
        super().save_model(request, obj, form, change)
        send_tracking_update_email(obj)

admin.site.register(HeroImage)  