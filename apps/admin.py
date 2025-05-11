import csv

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.utils import html

from apps.models import Category, Product, ProductImage

admin.site.site_header = "P29 Admin"
admin.site.site_title = "P29 Admin Portal"
admin.site.index_title = "Welcome to P29 Researcher Portal"

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = 'category',
    date_hierarchy = 'created_at'

    inlines = [ProductImageInline]
    list_per_page = 2
    list_display = 'id', 'name', 'quantity', 'is_quantity_enough'
    readonly_fields = 'is_quantity_enough',


    def has_add_permission(self, request):
        count = Product.objects.count()
        if count >= 1:
            return False
        return True


    def is_quantity_enough(self, obj):
        if obj.quantity > 0:
            return html.format_html("""<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="45" height="45" viewBox="0 0 45 45">
<path fill="#c8e6c9" d="M36,42H12c-3.314,0-6-2.686-6-6V12c0-3.314,2.686-6,6-6h24c3.314,0,6,2.686,6,6v24C42,39.314,39.314,42,36,42z"></path><path fill="#4caf50" d="M34.585 14.586L21.014 28.172 15.413 22.584 12.587 25.416 21.019 33.828 37.415 17.414z"></path>
</svg>""")
        else:
            return html.format_html("""<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="45" height="45" viewBox="0 0 45 45">
<path fill="#f44336" d="M44,24c0,11.045-8.955,20-20,20S4,35.045,4,24S12.955,4,24,4S44,12.955,44,24z"></path><path fill="#fff" d="M29.656,15.516l2.828,2.828l-14.14,14.14l-2.828-2.828L29.656,15.516z"></path><path fill="#fff" d="M32.484,29.656l-2.828,2.828l-14.14-14.14l2.828-2.828L32.484,29.656z"></path>
</svg>""")


class Technical(Product):
    class Meta:
        proxy = True
        verbose_name = 'Technical'
        verbose_name_plural = 'Technicals'

    def __str__(self):
        return self.name

@admin.register(Technical)
class TechnicalAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'price', 'quantity'
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(category__name='Technical')
        return queryset