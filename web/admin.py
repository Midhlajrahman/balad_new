from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Contact, CustomOrder, FAQ, Testimonial, Blog

admin.site.unregister(Group)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject")
    ordering = ("timestamp",)

    search_fields = (
        "first_name",
        "last_name",
    )


# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "position",
#     )


# @admin.register(CustomOrder)
# class CustomOrderAdmin(admin.ModelAdmin):
#     list_display = ("name", "phone")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)
    

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "position",
    )
    

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):  
    list_display = (
        "title",
        "date",
    )
    prepopulated_fields = {"slug": ("title",)}