from django import forms
from tinymce.widgets import TinyMCE

from main.models import District, ShippingFee, State
from products.models import (AvailableSize, Brands, Category,  # Colour,
                             Product, ProductImage, Review, Slider,
                             SubCategory, WeddingBanner)
from web.models import Testimonial


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            "name",
            "image",
            "slug",
            "status",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Category Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Category Slug", "class": "form-control"}
            ),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = "__all__"
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(
                attrs={"placeholder": "Sub Category Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Sub Category Slug", "class": "form-control"}
            ),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Product Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Product Slug", "class": "form-control"}
            ),
            "details": TinyMCE(attrs={"cols": 60, "rows": 10}),
            "meta_title": forms.TextInput(
                attrs={"placeholder": "Title", "class": "form-control"}
            ),
            "meta_description": forms.Textarea(
                attrs={"placeholder": "Description", "class": "form-control", "rows": 3}
            ),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brands": forms.Select(attrs={"class": "form-select"}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "color": forms.TextInput(
                attrs={"placeholder": "Color", "class": "form-control"}
            ),
            "sku": forms.TextInput(
                attrs={"placeholder": "Sku", "class": "form-control"}
            ),
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = (
            "name",
            "slug",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "State Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "State Slug", "class": "form-control"}
            ),
        }


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = (
            "name",
            "slug",
            "state",
            "delivery_charge",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter District Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "District Slug", "class": "form-control"}
            ),
            "state": forms.Select(attrs={"class": "form-select"}),
            "delivery_charge": forms.TextInput(
                attrs={
                    "placeholder": "Delivery Charge ",
                    "class": "form-control",
                    "type": "number",
                }
            ),
        }


class AvailableSizeForm(forms.ModelForm):
    class Meta:
        model = AvailableSize
        fields = (
            "unit",
            "sale_price",
            "regular_price",
            "is_stock",
        )
        widgets = {
            "unit": forms.Select(
                attrs={"class": "required form-select", "required": True}
            ),
            "sale_price": forms.TextInput(
                attrs={
                    "placeholder": "Sale Price ",
                    "class": "required form-control",
                    "type": "number",
                    "required": True,
                }
            ),
            "regular_price": forms.TextInput(
                attrs={
                    "placeholder": "Regular Price ",
                    "class": "required form-control",
                    "type": "number",
                    "required": True,
                }
            ),
            "is_stock": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input required",
                    "role": "switch",
                    "type": "checkbox",
                }
            ),
        }


# class ColourForm(forms.ModelForm):
#     class Meta:
#         model = Colour
#         fields = (
#             "name",
#             "image",
#             "hex_code",

#         )
#         widgets = {
#             "name": forms.TextInput(attrs={"placeholder": "Enter Color Name", "class": "form-control"}),
#             "image":forms.FileInput(attrs={"class": "file-input form-control"}),
#             "hex_code": forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),

#         }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image",)
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "file-input required", "type": "file", "required": True}
            ),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Below Average"),
        (3, "3 - Average"),
        (4, "4 - Good"),
        (5, "5 - Excellent"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Review
        exclude = ("created_at",)
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Full Name"}
            ),
            "headline": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "What’s most important to know",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What did you like or dislike? What did you use this product for?",
                }
            ),
        }


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ("title", "image", "category", "is_active")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class WeddingForm(forms.ModelForm):
    class Meta:
        model = WeddingBanner
        fields = ("name", "slug", "banner_image", "category", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(
                attrs={"placeholder": "Banner Slug", "class": "form-control"}
            ),
            "banner_image": forms.FileInput(attrs={"class": "file-input"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ShippingFeeForm(forms.ModelForm):
    class Meta:
        model = ShippingFee
        fields = ("name", "price")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ("name", "position", "description")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class BrandsForm(forms.ModelForm):
    class Meta:
        model = Brands
        fields = ("brand_name", "brand_image")
        widgets = {
            "brand_name": forms.TextInput(attrs={"class": "form-control"}),
            "brand_image": forms.FileInput(attrs={"class": "file-input"}),
        }
