from datetime import datetime, timedelta

from django import forms
# models
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
# view
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

# forms
from main.forms import (AvailableSizeForm, BrandsForm,  # ColourForm,
                        CategoryForm, DistrictForm, ProductForm,
                        ProductImageForm, ReviewForm, ShippingFeeForm,
                        SliderForm, StateForm, SubCategoryForm,
                        TestimonialForm, BlogForm, FAQForm)
from main.mixins import LoginRequiredMixin, SuperAdminLoginRequiredMixin
from main.models import District, ShippingFee, State
from order.models import Order
from products.models import (AvailableSize, Brands, Category,  # Colour,
                             Product, ProductImage, Review, Slider,
                             SubCategory, WeddingBanner)
from web.forms import ContactForm
from web.models import Contact, CustomOrder, Testimonial, Blog, FAQ


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    extra_context = {"is_dashbord": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        context["last_two_week_orders_count"] = Order.objects.filter(
            created__gte=two_weeks_ago
        ).count()
        context["last_two_week_reviews_count"] = Review.objects.filter(
            created_at__gte=two_weeks_ago
        ).count()
        context["last_two_week_customers_count"] = User.objects.filter(
            date_joined__gte=two_weeks_ago
        ).count()
        context["orders"] = Order.objects.filter(is_ordered=False).order_by("-id")[:100]
        context["customers"] = User.objects.order_by("-id")[:100]
        context["reviews"] = Review.objects.order_by("-id")[:100]
        return context


# order
class OrderView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/order/list.html"
    model = Order
    extra_context = {"is_order": True}

    def get_queryset(self):
        return self.model.objects.filter(is_ordered=False)


class OrderDetailView(SuperAdminLoginRequiredMixin, DetailView):
    model = Order
    template_name = "dashboard/order/single.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"is_order": True}


class InvoiceView(SuperAdminLoginRequiredMixin, DetailView):
    model = Order
    template_name = "account/invoice.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"is_order": True}


class OrderUpdateView(SuperAdminLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status = request.GET.get("status")
        pk = request.GET.get("pk")
        order = get_object_or_404(Order, pk=pk)
        order.order_status = status
        order.save()
        message = "Order status updated successfully"
        response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": str(message),
            "reload": "true",
        }

        return JsonResponse(response_data)


# State
class StateListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/state/list.html"
    model = State
    extra_context = {"is_state": True}


class StateCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = State
    template_name = "dashboard/state/entry.html"
    form_class = StateForm
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True, "title": "Add New State"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "State Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class StateUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = State
    template_name = "dashboard/state/entry.html"
    form_class = StateForm
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True, "title": "State Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "State Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class StateDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = State
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True}


# District
class DistrictListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/district/list.html"
    model = District
    extra_context = {"is_district": True}


class DistrictCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = District
    template_name = "dashboard/district/entry.html"
    form_class = DistrictForm
    success_url = reverse_lazy("main:districts")
    extra_context = {"is_district": True, "title": "Add New District"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "District Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class DistrictUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = District
    template_name = "dashboard/district/entry.html"
    form_class = DistrictForm
    success_url = reverse_lazy("main:districts")
    extra_context = {"is_district": True, "title": "District Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "District Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class DistrictDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = District
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:districts")


# category
class CategoryListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/category/list.html"
    model = Category
    extra_context = {"is_category": True, "is_category_list": True}


class CategoryCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Category
    template_name = "dashboard/category/entry.html"
    form_class = CategoryForm
    success_url = reverse_lazy("main:categories")
    extra_context = {
        "is_category": True,
        "is_category_create": True,
        "title": "Add New Category",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryUpdate(SuperAdminLoginRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category/entry.html"
    form_class = CategoryForm
    success_url = reverse_lazy("main:categories")
    extra_context = {"is_category": True, "is_edit": True, "title": "Edit Category"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:categories")
    extra_context = {"is_category": True}


# product
class ProductListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/product/list.html"
    model = Product
    extra_context = {"is_product": True, "is_product_list": True}


class CreateProductView(SuperAdminLoginRequiredMixin, View):
    template_name = "dashboard/product/entry.html"
    form_class = ProductForm
    available_size_formset_class = formset_factory(
        AvailableSizeForm, extra=1, can_delete=True
    )
    product_image_formset_class = formset_factory(
        ProductImageForm, extra=1, can_delete=True
    )

    # colour_formset_class = formset_factory(ColourForm,extra=1,can_delete=True)
    def get(self, request, *args, **kwargs):
        available_size_formset = self.available_size_formset_class(
            prefix="available_size_formset"
        )
        product_image_formset = self.product_image_formset_class(
            prefix="product_image_formset"
        )
        # colour_formset = self.colour_formset_class(prefix="colour_formset")
        product_form = self.form_class()
        context = {
            "is_product": True,
            "is_product_create": True,
            "title": "Add New Product",
            "available_size_formset": available_size_formset,
            "product_image_formset": product_image_formset,
            # "colour_formset": colour_formset,
            "form": product_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product_image_formset = self.product_image_formset_class(
            request.POST, request.FILES, prefix="product_image_formset"
        )
        available_size_formset = self.available_size_formset_class(
            request.POST, prefix="available_size_formset"
        )
        # colour_formset = self.colour_formset_class(request.POST, request.FILES ,prefix="colour_formset")
        # print(colour_formset)
        product_form = self.form_class(request.POST, request.FILES)

        # if available_size_formset.is_valid() and product_form.is_valid() and product_image_formset.is_valid() and colour_formset.is_valid():

        if (
            available_size_formset.is_valid()
            and product_form.is_valid()
            and product_image_formset.is_valid()
        ):
            product = product_form.save()

            for size_form in available_size_formset:
                size_data = size_form.save(commit=False)
                size_data.product = product
                size_data.save()

            for image_form in product_image_formset:
                image_data = image_form.save(commit=False)
                image_data.product = product
                image_data.save()

            # for colour_form in colour_formset:
            #     colour_data = colour_form.save(commit=False)
            #     colour_data.product = product
            #     colour_data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Product Created successfully.",
            }
            return JsonResponse(response_data)
        else:
            message = ""
            if product_form.errors:
                message += str(product_form.errors)
            if available_size_formset.errors:
                message += str(available_size_formset.errors)
            if product_image_formset.errors:
                message += str(product_image_formset.errors)
            # if colour_formset.errors:
            #     message += str(colour_formset.errors)

            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": message,
            }
            return JsonResponse(response_data)


def edit_product(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    if ProductImage.objects.filter(product=instance).exists():
        extra = 0
    else:
        extra = 1

    ProductImageFormSet = inlineformset_factory(
        Product,
        ProductImage,
        can_delete=True,
        extra=extra,
        fields=("image",),
        widgets={
            "image": forms.FileInput(
                attrs={"class": "file-input required", "type": "file"}
            ),
        },
    )
    if AvailableSize.objects.filter(product=instance).exists():
        extra = 0
    else:
        extra = 1

    AvailableSizeFormSet = inlineformset_factory(
        Product,
        AvailableSize,
        can_delete=True,
        extra=extra,
        fields="__all__",
        widgets={
            "weight": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Weight",
                    "class": "required form-control",
                    "type": "number",
                }
            ),
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
        },
    )
    # if Colour.objects.filter(product=instance).exists():
    #     extra = 0
    # else:
    #     extra = 1

    # ColourFormSet= inlineformset_factory(
    #     Product,
    #     # Colour,
    #     can_delete=True,
    #     extra=extra,
    #     fields="__all__",
    #     widgets = {
    #         "name": forms.TextInput(attrs={"placeholder": "Enter Color Name", "class": "form-control"}),
    #         "image":forms.FileInput(attrs={"class": "file-input form-control"}),
    #         "hex_code": forms.TextInput(attrs={"placeholder": "", "class": "form-control"}),

    #     }
    # )

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        product_image_formset = ProductImageFormSet(
            request.POST,
            request.FILES,
            prefix="product_image_formset",
            instance=instance,
        )
        available_size_formset = AvailableSizeFormSet(
            request.POST, prefix="available_size_formset", instance=instance
        )
        # colour_formset = ColourFormSet(request.POST,request.FILES,prefix="colour_formset",instance=instance)
        if form.is_valid():

            data = form.save(commit=False)
            data.save()
            if product_image_formset.is_valid():
                ProductImage.objects.filter(product=data.pk).delete()
                for f1 in product_image_formset:
                    print(f1)
                    data1 = f1.save(commit=False)
                    data1.product = data
                    data1.save()

            if available_size_formset.is_valid():
                AvailableSize.objects.filter(product=data.pk).delete()
                for f0 in available_size_formset:
                    data2 = f0.save(commit=False)
                    data2.product = data
                    data2.save()
            # if colour_formset.is_valid():
            #     Colour.objects.filter(product=data.pk).delete()
            #     for f3 in colour_formset:
            #         data3 = f3.save(commit=False)
            #         data3.product=data
            #         data3.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Product Updated successfully.",
            }
            return JsonResponse(response_data)

        else:
            message = ""
            if form.errors:
                message += str(form.errors)
            if available_size_formset.errors:
                message += str(available_size_formset.errors)
            if product_image_formset.errors:
                message += str(product_image_formset.errors)
            # if colour_formset.errors:
            #     message += str(colour_formset.errors)

            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": message,
            }
            return JsonResponse(response_data)
    else:
        form = ProductForm(instance=instance)
        product_image_formset = ProductImageFormSet(
            prefix="product_image_formset", instance=instance
        )
        available_size_formset = AvailableSizeFormSet(
            prefix="available_size_formset", instance=instance
        )
        # colour_formset = ColourFormSet(prefix="colour_formset",instance=instance)
        context = {
            "form": form,
            "product": instance,
            "title": "Edit Product",
            "is_edit": True,
            "product_image_formset": product_image_formset,
            "available_size_formset": available_size_formset,
            # "colour_formset": colour_formset,
        }
        return render(request, "dashboard/product/entry.html", context)


class ProductDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = Product
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:product_list")
    extra_context = {"is_product": True}


# customer
class CustomerListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/customer/list.html"
    model = User
    extra_context = {"is_customer": True}


# review
class ReviewListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/review/list.html"
    model = Review
    extra_context = {"is_review": True}


class ReviewCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Review
    template_name = "dashboard/review/entry.html"
    form_class = ReviewForm
    success_url = reverse_lazy("main:review_list")
    extra_context = {"is_review": True, "title": "Add New Review"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Review Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ReviewUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Review
    template_name = "dashboard/review/entry.html"
    form_class = ReviewForm
    success_url = reverse_lazy("main:review_list")
    extra_context = {"is_review": True, "title": "Edit Review"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Review Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ReviewDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Review
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:review_list")


# Slider


class SliderListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/slider/list.html"
    model = Slider
    extra_context = {"is_slider": True}


class SliderCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Slider
    template_name = "dashboard/slider/entry.html"
    form_class = SliderForm
    success_url = reverse_lazy("main:sliders")
    extra_context = {"is_slider": True, "title": "Add New Slider"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Slider Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SliderUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Slider
    template_name = "dashboard/slider/entry.html"
    form_class = SliderForm
    success_url = reverse_lazy("main:sliders")
    extra_context = {"is_slider": True, "title": "Slider Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Slider Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SliderDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Slider
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:sliders")


# Shipping Fee


class ShippingListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/shipping/list.html"
    model = ShippingFee
    extra_context = {"is_shipping": True}


class ShippingCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = ShippingFee
    template_name = "dashboard/shipping/entry.html"
    form_class = ShippingFeeForm
    success_url = reverse_lazy("main:shippingfees")
    extra_context = {"is_shipping": True, "title": "Add New Shipping Fee"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Shipping Fee Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ShippingUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = ShippingFee
    template_name = "dashboard/shipping/entry.html"
    form_class = ShippingFeeForm
    success_url = reverse_lazy("main:shippingfees")
    extra_context = {"is_shipping": True, "title": "Shipping Fee Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Shipping Fee Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ShippingDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = ShippingFee
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:shippingfees")


# contact
class ContactListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/contact/list.html"
    model = Contact
    extra_context = {"is_contact": True}


class ContactCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Contact
    template_name = "dashboard/contact/entry.html"
    form_class = ContactForm
    success_url = reverse_lazy("main:contacts")
    extra_context = {"is_contact": True, "title": "Add New Contact"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Contact Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ContactUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Contact
    template_name = "dashboard/contact/entry.html"
    form_class = ContactForm
    success_url = reverse_lazy("main:contacts")
    extra_context = {"is_contact": True, "title": "Contact Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Contact Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ContactDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:contacts")


# testimonial


class TestimonialListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/testimonial/list.html"
    model = Testimonial
    extra_context = {"is_testimonial": True}


class TestimonialCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Testimonial
    template_name = "dashboard/testimonial/entry.html"
    form_class = TestimonialForm
    success_url = reverse_lazy("main:testimonials")
    extra_context = {"is_testimonial": True, "title": "Add New Testimonial"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Testimonial Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TestimonialUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Testimonial
    template_name = "dashboard/testimonial/entry.html"
    form_class = TestimonialForm
    success_url = reverse_lazy("main:testimonials")
    extra_context = {"is_testimonial": True, "title": "Testimonial Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Testimonial Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TestimonialDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Testimonial
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:testimonials")


# Blog


class BlogListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/blog/list.html"
    model = Blog
    extra_context = {"is_blog": True}


class BlogCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Blog
    template_name = "dashboard/blog/entry.html"
    form_class = BlogForm
    success_url = reverse_lazy("main:blogs")
    extra_context = {"is_blog": True, "title": "Add New Blog"}

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')  # Ensure image is saved
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Testimonial Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BlogUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Blog
    template_name = "dashboard/blog/entry.html"
    form_class = BlogForm
    success_url = reverse_lazy("main:blogs")
    extra_context = {"is_blog": True, "title": "Blog Update"}

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Blog Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BlogDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:blogs")


# FAQ


class FAQListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/faq/list.html"
    model = FAQ
    extra_context = {"is_faq": True}


class FAQCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = FAQ
    template_name = "dashboard/faq/entry.html"
    form_class = FAQForm
    success_url = reverse_lazy("main:faqs")
    extra_context = {"is_faq": True, "title": "Add New FAQ"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Testimonial Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class FAQUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = FAQ
    template_name = "dashboard/faq/entry.html"
    form_class = FAQForm
    success_url = reverse_lazy("main:faqs")
    extra_context = {"is_faq": True, "title": "FAQ Update"}

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "FAQ Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class FAQDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = FAQ
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:faqs")
    

# sub category
class SubCategoryListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/subcategory/list.html"
    model = SubCategory
    extra_context = {"is_sub_category": True, "is_sub_category_list": True}


class SubCategoryCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = SubCategory
    template_name = "dashboard/subcategory/entry.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("main:sub_categories")
    extra_context = {
        "is_sub_category": True,
        "is_sub_category_create": True,
        "title": "Add New sub Category",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SubCategoryUpdate(SuperAdminLoginRequiredMixin, UpdateView):
    model = SubCategory
    template_name = "dashboard/subcategory/entry.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("main:sub_categories")
    extra_context = {"is_subcategory": True, "is_edit": True, "title": "Edit Category"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "SubCategory Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SubCategoryDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = SubCategory
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:sub_categories")
    extra_context = {"is_subcategory": True}


# Custom Order
class CustomOrderView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/custom_order/list.html"
    model = CustomOrder


class CustomOrderDetailView(SuperAdminLoginRequiredMixin, DetailView):
    model = CustomOrder
    template_name = "dashboard/custom_order/single.html"
    context_object_name = "order"
    slug_field = "id"
    slug_url_kwarg = "order_id"
    extra_context = {"is_custom_order": True}


class CustomOrderUpdateView(SuperAdminLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status = request.GET.get("status")
        pk = request.GET.get("pk")
        order = get_object_or_404(Order, pk=pk)
        order.order_status = status
        order.save()
        message = "Order status updated successfully"
        response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": str(message),
            "reload": "true",
        }

        return JsonResponse(response_data)


# class WeddingListView(SuperAdminLoginRequiredMixin, ListView):
#     template_name = "dashboard/wedding/list.html"
#     model = WeddingBanner
#     extra_context = {"is_wedding": True}


# class WeddingCreateView(SuperAdminLoginRequiredMixin, CreateView):
#     model = WeddingBanner
#     template_name = "dashboard/wedding/entry.html"
#     form_class = WeddingForm
#     success_url = reverse_lazy("main:wedding_create")
#     extra_context = {"is_wedding": True, "title": "Add New Wedding Banner"}

#     def form_valid(self, form):
#         response_data = super().form_valid(form)
#         response_data = {
#             "status": "true",
#             "title": "Successfully Submitted",
#             "message": "Wedding Banner Created successfully.",
#         }
#         return JsonResponse(response_data)

#     def form_invalid(self, form):
#         response_data = super().form_invalid(form)
#         response_data = {
#             "status": "false",
#             "title": "Form validation error",
#             "message": str(form.errors),
#         }
#         return JsonResponse(response_data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["is_edit"] = (
#             self.object is not None
#         )  # Check if editing an existing object
#         context["wedding"] = self.object  # Pass the object to the template
#         return context


# class WeddingUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
#     model = WeddingBanner
#     template_name = "dashboard/wedding/entry.html"
#     form_class = WeddingForm
#     success_url = reverse_lazy("main:wedding_update")
#     extra_context = {"is_wedding": True, "title": "Wedding Banner Update"}

#     def form_valid(self, form):
#         response_data = super().form_valid(form)
#         response_data = {
#             "status": "true",
#             "title": "Successfully Submitted",
#             "message": "Wedding Banner Updated successfully.",
#         }
#         return JsonResponse(response_data)

#     def form_invalid(self, form):
#         response_data = super().form_invalid(form)
#         response_data = {
#             "status": "false",
#             "title": "Form validation error",
#             "message": str(form.errors),
#         }
#         return JsonResponse(response_data)


# class WeddingDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
#     model = WeddingBanner
#     template_name = "dashboard/commen/delete.html"
#     success_url = reverse_lazy("main:wedding")


class BrandsListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/brands/list.html"
    model = Brands
    extra_context = {"is_brands": True}


class BrandsCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Brands
    template_name = "dashboard/brands/entry.html"
    form_class = BrandsForm
    success_url = reverse_lazy("main:brands_create")
    extra_context = {"is_brands": True, "title": "Add New Brand"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Brand Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BrandsUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Brands
    template_name = "dashboard/brands/entry.html"
    form_class = BrandsForm
    success_url = reverse_lazy("main:brands_update")
    extra_context = {"is_brands": True, "title": "Brand Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Brand Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BrandsDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Brands
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:brands")


class LoadSubcategoriesView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get("category_id")
        subcategories = SubCategory.objects.filter(category_id=category_id).values(
            "id", "name"
        )
        return JsonResponse(list(subcategories), safe=False)
