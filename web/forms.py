from django import forms
from django.forms import widgets

from .models import Contact, CustomOrder


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("timestamp",)
        widgets = {
            "name": widgets.TextInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Your Name",
                    "required": True,
                }
            ),
            "phone": widgets.TextInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Your Phone",
                    "required": True,
                }
            ),
            "email": widgets.EmailInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Your Email Address",
                    "required": True,
                }
            ),
            "subject": widgets.TextInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Subject",
                    "required": True,
                }
            ),
            "message": widgets.Textarea(
                attrs={
                    "class": "required form-control",
                    "cols": "30",
                    "rows": "10",
                    "placeholder": "Type Your Message",
                    "required": True,
                }
            ),
        }


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = [
            "name",
            "phone",
            "email",
            "address",
            "front_neck_depth",
            "back_neck_depth",
            "bust",
            "waist",
            "sleeve_length",
            "shoulder_length",
            "full_length",
            "product_name",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full name"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email address"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Delivery Address",
                    "rows": 3,
                }
            ),
            "front_neck_depth": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Front neck depth in inches",
                }
            ),
            "back_neck_depth": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Back neck depth in inches",
                }
            ),
            "bust": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Bust measurement in inches",
                }
            ),
            "waist": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Waist measurement in inches",
                }
            ),
            "sleeve_length": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sleeve length in inches",
                }
            ),
            "shoulder_length": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Shoulder length in inches",
                }
            ),
            "full_length": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Full length in inches"}
            ),
            "product_name": forms.HiddenInput(),
        }
