from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import (
    AvailableSize,
    Category,
    Product,
    ProductImage,
    Review,
    Slider,
    Colour,
    SubCategory,
    FestivalSeason,
    Brands
   
)

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">')
        return None

    image_preview.short_description = "Image Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "status")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("status",)
    search_fields = ("name",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">')
        return None

    image_preview.short_description = "Image Preview"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 1

class ColorInLine(admin.TabularInline):
    model = Colour
    extra=1

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status")
    prepopulated_fields = {"slug": ("name",)}

    def save_model(self, request, obj, form, change):
        # Generate slug if it's not set or ensure uniqueness
        if not obj.slug:
            base_slug = slugify(obj.name)
            unique_slug = base_slug
            counter = 1
            # Check for existing slugs in the same category
            while SubCategory.objects.filter(category=obj.category, slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = unique_slug
        # Save the object
        super().save_model(request, obj, form, change)

@admin.register(FestivalSeason)
class FestivalSeasonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "image_preview", "category", "is_active","sku")
    exclude = ("creator",)
    list_filter = (
        "category",
        "is_popular",
       
    )
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    autocomplete_fields = ("category",)
    inlines = [ProductImageInline, AvailableSizeInline,ColorInLine]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">')
        return None

    def sale_price(self, obj):
        return obj.get_sale_price()
    
   

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Dynamically filter subcategory queryset
        if obj and obj.category:
            form.base_fields['subcategory'].queryset = SubCategory.objects.filter(category=obj.category)
        else:
            form.base_fields['subcategory'].queryset = SubCategory.objects.none()
        return form

    image_preview.short_description = "Image Preview"
    sale_price.short_description = "Sale Price"


@admin.register(AvailableSize)
class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        # "size",
        "unit",
        "sale_price",
        "regular_price",
        "is_stock",
    )
    list_filter = ("product", "unit", "is_stock")

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ["product", "approval", "created_at"]
#     list_filter = ["approval", "created_at"]
#     search_fields = ["content", "user__username", "product__title"]
#     actions = ["approve_comments"]

#     def approve_comments(self, request, queryset):
#         queryset.update(approved=True)

#     approve_comments.short_description = "Approve selected comments"

@admin.register(Brands)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)