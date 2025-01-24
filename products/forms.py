from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["fullname","headline","content"]
        widgets = {
            "fullname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Full Name"}),
            "headline": forms.TextInput(attrs={"class": "form-control", "placeholder": "title"}),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What did you like or dislike? What did you use this product for?",
                }
            ),
        }

# class ProductCustomizationForm(forms.ModelForm):
#     class Meta:
#         model = ProductCustomization
#         fields = ['product', 'box', 'message']