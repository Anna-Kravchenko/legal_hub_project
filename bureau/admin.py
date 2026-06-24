from django.contrib import admin
from .models import Client, Service, Language, Review, Order, ServiceCategory


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price', 'completion_time', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'completion_time', 'is_active')

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')
    search_fields = ('client_name', 'text')
    list_editable = ('is_published',)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'service',
        'source_language',
        'target_language',
        'status',
        'created_at',
    )
    list_filter = ('status', 'service', 'source_language', 'target_language')
    search_fields = ('client__name', 'client__email', 'comment')
    ordering = ('-created_at',)
    list_editable = ('status',)

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)