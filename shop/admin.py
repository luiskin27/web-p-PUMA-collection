# shop/admin.py
from django.contrib import admin
from .models import Category, Product, ShoeSize, ClothingSize

@admin.register(ShoeSize)
class ShoeSizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    search_fields = ['size']

@admin.register(ClothingSize)
class ClothingSizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    search_fields = ['size']


from django.contrib import admin
from .models import Category, Product, ShoeSize, ClothingSize

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'product_type', 'created']
    list_filter = ['product_type', 'available', 'created']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    filter_horizontal = ('shoe_sizes', 'clothing_sizes')

    # ВОЛШЕБСТВО: все размеры уже выбраны!
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.product_type == 'shoes':
            form.base_fields['shoe_sizes'].initial = ShoeSize.objects.all()
        elif obj and obj.product_type == 'clothing':
            form.base_fields['clothing_sizes'].initial = ClothingSize.objects.all()
        return form

    # При сохранении — если ничего не выбрано, ставим все размеры
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.product_type == 'shoes' and not obj.shoe_sizes.exists():
            obj.shoe_sizes.set(ShoeSize.objects.all())
        elif obj.product_type == 'clothing' and not obj.clothing_sizes.all():
            obj.clothing_sizes.set(ClothingSize.objects.all())