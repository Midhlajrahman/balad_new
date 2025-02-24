import urllib.parse
from decimal import Decimal, InvalidOperation

# PHONEPAY
import razorpay
from dal import autocomplete
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView

from main.mixins import LoginRequiredMixin
from main.models import District
from order.forms import OrderForm
from order.models import Order, OrderItem
from products.models import (AvailableSize, Brands, Category, Product,
                             ProductImage, Slider, SubCategory, WeddingBanner)
# CART
from web.cart import Cart
# form
from web.forms import ContactForm, MeasurementForm
# model
from web.models import Testimonial, FAQ, Blog

client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET))


class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instances = Product.objects.filter(is_active=True)
        product_cats = instances
        categories = Category.objects.exclude(name="Customized Giftbox")
        query = self.request.GET.get("q", "")
        if query:
            print('query=',query)
            instances = instances.filter(name__icontains=query)
            product_cats = instances
        context["categories"] = categories
        context["products"] = instances
        context["sliders"] = Slider.objects.filter(is_active=True)
        context["sale"] = Product.objects.filter(is_sale=True)
        context["new_arrival"] = Product.objects.all().order_by("-id")
        context["product_cat"] = product_cats
        context["display_women_sub_category"] = SubCategory.objects.filter(
            is_display_sub_category=True, category__name="Women"
        )
        context["display_men_sub_category"] = SubCategory.objects.filter(
            is_display_sub_category=True, category__name="Men"
        )
        context["season"] = WeddingBanner.objects.all()
        context["brands"] = Brands.objects.filter(is_brand_display=True)

        # Add category products to context
        category_products = {
            category: category.get_products() for category in categories
        }
        context["category_products"] = category_products

        return context

class AboutView(TemplateView):
    template_name = "web/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["testimonials"] = Testimonial.objects.all()
        context["brands"] = Brands.objects.filter(is_brand_display=True)
        context["faqs"] = FAQ.objects.all()
        return context
    
class BlogView(TemplateView):
    template_name = "web/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = "web/blog-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all()
        return context
    
    
class ShopView(ListView):
    model = Product
    template_name = "web/shop.html"
    context_object_name = "products"

    def get_queryset(self):
        products = Product.objects.filter(is_active=True)
        query = self.request.GET.get("q", "")
        if query:
            products = products.filter(name__icontains=query)
        category_title = None
        self.category_title = category_title if category_title else None
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context["categories"] = Category.objects.all()
        context["title"] = self.category_title
        context["most_review"] = qs.annotate(num_reviews=Count("reviews"))
        # context['all_colors'] = Colour.objects.distinct()
        # context['products'] = Product.objects.prefetch_related('colour_set')
        context["products"] = qs
        context["all_brands"] = Brands.objects.all()

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "web/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Cart logic
        cart = Cart(self.request)
        cart_items = []
        form = MeasurementForm()

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(AvailableSize, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["sale_price"]) * quantity
            cart_items.append(
                {
                    "product": variant,
                    "quantity": quantity,
                    "total_price": total_price,
                }
            )

        # Add cart data to context
        context["cart_items"] = cart_items
        context["cart_total"] = sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in cart.get_cart()
        )

        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = MeasurementForm(request.POST)

        if form.is_valid():
            # Save the form data to the backend
            custom_order = form.save(commit=False)
            custom_order.product_name = (
                product.name
            )  # Save product name from the Product model
            custom_order.save()

            # Get the form data
            form_data = form.cleaned_data
            name = form_data["name"]
            phone = form_data["phone"]
            email = form_data["email"]
            address = form_data["address"]
            front_neck_depth = form_data["front_neck_depth"]
            back_neck_depth = form_data["back_neck_depth"]
            bust = form_data["bust"]
            waist = form_data["waist"]
            sleeve_length = form_data["sleeve_length"]
            shoulder_length = form_data["shoulder_length"]
            full_length = form_data["full_length"]
            product_name = form_data["product_name"]

            # Construct WhatsApp message
            message = (
                f"Customisation Order Details:\n\n"
                f"Product Name: {product_name}\n"
                f"Name: {name}\n"
                f"Phone: {phone}\n"
                f"Email: {email}\n"
                f"Address: {address}\n\n"
                f"Measurements:\n"
                f"Front Neck Depth: {front_neck_depth} inches\n"
                f"Back Neck Depth: {back_neck_depth} inches\n"
                f"Bust: {bust} inches\n"
                f"Waist: {waist} inches\n"
                f"Sleeve Length: {sleeve_length} inches\n"
                f"Shoulder Length: {shoulder_length} inches\n"
                f"Full Length: {full_length} inches\n\n"
            )

            # Encode message for WhatsApp URL
            encoded_message = urlencode({"text": message})
            whatsapp_number = (
                "+918589005600"  # Replace with your business WhatsApp number
            )
            whatsapp_url = f"https://wa.me/{whatsapp_number}?{encoded_message}"

            # Redirect user to WhatsApp
            return redirect(whatsapp_url)

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            "is_contact": True,
            "form": form,
        }
        return render(request, "web/contact.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully Submitted",
            }
        else:
            messege = {}
            for key, error in list(form.errors.items()):
                if key == "captcha" and error[0] == "This field is required.":
                    messege = "Please check the captcha"
                else:
                    messege = error

            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": messege,
            }
            print(form.errors.items())
        return JsonResponse(response_data)


# CART
def cart_view(request):
    cart = Cart(request)
    cart_items = []

    for item_id, item_data in cart.get_cart():
        variant = get_object_or_404(AvailableSize, id=item_id)
        quantity = item_data["quantity"]
        total_price = Decimal(item_data["sale_price"]) * quantity
        cart_items.append(
            {
                "product": variant,
                "quantity": quantity,
                "total_price": total_price,
            }
        )
    context = {
        "cart_items": cart_items,
        "cart_total": sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in cart.get_cart()
        ),
    }

    return render(request, "web/cart.html", context)


def cart_add(request):
    cart = Cart(request)
    cart_instance = cart.cart
    quantity = request.GET.get("quantity", 1)
    product_id = request.GET.get("product_id", "")
    print("product_id=", product_id)
    print(quantity)
    variant = get_object_or_404(AvailableSize, pk=product_id)
    cart.add(variant, quantity=int(quantity))
    print(cart_instance)

    # Prepare cart items for rendering
    cart_items = [
        {
            "quantity": item["quantity"],
            "sale_price": item["sale_price"],
        }
        for item in cart_instance.values()
    ]

    # Render updated modal HTML
    cart_modal_html = render_to_string(
        "web/includes/cart_modal.html", {"cart_items": cart_items}
    )

    return JsonResponse(
        {
            "message": "Product Quantity Added from cart successfully",
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(cart_instance[product_id]),
            "cart_total": cart.cart_total(),
            "cart_count": len(cart_instance),
            "cart_modal_html": cart_modal_html,
        }
    )

def clear_cart_item(request, item_id):
    cart = Cart(request)
    variant = get_object_or_404(AvailableSize, id=item_id)
    cart.remove(variant)
    return redirect(reverse("web:cart"))

def minus_to_cart(request):
    cart = Cart(request)
    cart_instance = cart.cart
    item_id = request.GET.get("item_id")
    variant = get_object_or_404(AvailableSize, id=item_id)
    cart.decrease_quantity(variant)
    return JsonResponse(
        {
            "message": "Product Quantity decreased from cart successfully",
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(cart_instance[item_id]),
            "cart_total": cart.cart_total(),
        }
    )


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("web:shop"))

def order(request):
    if request.method == "POST":
        cart = Cart(request)
        products = ""
        total = 0
        counter = 1
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(AvailableSize, id=item_id)
            quantity = item_data["quantity"]
            price = Decimal(item_data["sale_price"])
            if variant.product.category.is_combo:
                products += f"{counter}.{variant.product.name} ({quantity}x{price}) ₹ {variant.weight*quantity} \n ----------------------- \n"
            else:
                products += f"{counter}.{variant.product.name}-{variant.weight} {variant.unit} ({quantity}x{price}) ₹ {variant.sale_price*quantity} \n ----------------------- \n"
            total += quantity * variant.sale_price
            counter += 1

        message = (
            f"============================\n"
            f"Welcome to balad.\n"
            f"============================\n\n"
            f'Name: {request.POST.get("name")}\n'
            f'Phone: {request.POST.get("phone")}\n'
            f'Address: {request.POST.get("address")}\n'
            f"----------------------------\n\n"
            f"Products:\n"
            f"{products}\n\n"
            f"Grand Total: {total}\n"
            f"============================\n"
            f"Thank you for placing your order with balad. Your order has been confirmed.your order will be delivered in 7 working days.\n"
            f"Thank you for shopping with us.\n "
        )

        whatsapp_api_url = "https://api.whatsapp.com/send"
        phone_number = "+918589005600"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"
        cart.clear()
        return redirect(whatsapp_url)


def parse_decimal(value, default=0):
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)


class CheckoutView(View):
    template_name = "web/shop-checkout.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        form = OrderForm()

        context = {
            "cart_items": cart_items,
            "cart_total": sum(item["total_price"] for item in cart_items),
            "form": form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST)
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)

        subtotal = sum(item["total_price"] for item in cart_items)
        if form.is_valid():
            data = form.save(commit=False)
            data.subtotal = subtotal
            data.save()

            # Save cart items as order items
            for item_id, item_data in cart.get_cart():
                variant = get_object_or_404(AvailableSize, id=item_id)
                quantity = item_data["quantity"]
                price = Decimal(item_data["sale_price"])
                sku = variant.product.sku if variant.product.sku else "N/A"
                color = variant.product.color if variant.product.color else "N/A"

                order_item = OrderItem.objects.create(
                    order=data,
                    product=variant,
                    price=price,
                    quantity=quantity,
                    sku=sku,
                    color=color,
                )
                order_item.save()

            # Construct the message body
            message_body = (
                f"Order Confirmation\n\n"
                f"Order ID: {data.id}\n"
                f"Name: {data.full_name}\n"
                f"Address Line 1: {data.address_line_1}\n"
                f"Address Line 2: {data.address_line_2}\n"
                f"City: {data.city}\n"
                f"District: {data.district}\n"
                f"State: {data.state}\n"
                f"Pin Code: {data.pin_code}\n"
                f"Mobile: {data.mobile_no}\n"
                f"Email: {data.email}\n\n"
                f"Items:\n"
            )
            # Append items to the message body
            for item in cart_items:
                message_body += (
                    f"- {item['variant'].product} (x{item['quantity']}): {item['total_price']} INR\n"
                    f"  SKU: {item['variant'].product.sku if item['variant'].product.sku else 'N/A'}\n"
                    f"  Color: {item['variant'].product.color if item['variant'].product.color else 'N/A'}\n\n"
                )
            message_body += f"\nSubtotal: {data.subtotal} INR"

            # Send message via WhatsApp
            whatsapp_api_url = "https://api.whatsapp.com/send"
            phone_number = "+919447425555"
            encoded_message = urllib.parse.quote(message_body)
            whatsapp_url = (
                f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"
            )

            cart.clear()
            return redirect(whatsapp_url)

        else:
            context = {
                "cart_items": cart_items,
                "cart_total": sum(item["total_price"] for item in cart_items),
                "form": form,
            }
            return render(request, self.template_name, context)

    def get_cart_items(self, cart):
        cart_items = []
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(AvailableSize, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["sale_price"]) * quantity
            cart_items.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "total_price": total_price,
                }
            )
        return cart_items

class PaymentView(View):
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        currency = "INR"
        amount = float(order.payable) * 100
        razorpay_order = client.order.create(
            {"amount": amount, "currency": currency, "payment_capture": "1"}
        )
        razorpay_order_id = razorpay_order["id"]
        order.razorpay_order_id = razorpay_order_id
        order.save()
        context = {
            "object": order,
            "amount": amount,
            "razorpay_key": settings.RAZOR_PAY_KEY,
            "razorpay_order_id": razorpay_order_id,
            "callback_url": f"{settings.DOMAIN}/callback/{order.pk}/",
        }
        return render(request, "web/payment.html", context=context)


@csrf_exempt
def callback(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        response_data = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature_id
        client = razorpay.Client(
            auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET)
        )
        result = client.utility.verify_payment_signature(response_data)

        if result is not None:
            print("Signature verification successful")
            order.is_ordered = True
            order.order_status = "Placed"
            order.payment_status = "Success"
            order.save()

            products = ""
            total = 0
            counter = 1
            for item in order.get_items():

                products += f"{counter}.{item.product.product.name}-{item.product.weight} {item.product.unit} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
                total += item.subtotal()
                counter += 1

            message = (
                f"============================\n"
                f"Order Confirmed\n"
                f"============================\n\n"
                f"Order ID: {order.order_id}\n"
                f"Order Date: {order.created}\n"
                f"Order Status: Placed\n"
                f"Payment Method: Online Payment\n"
                f"Payment Status: Success\n"
                f"----------------------------\n\n"
                f"Products:\n\n"
                f"{products}\n\n"
                f"----------------------------\n\n"
                f"Order Summary:\n\n"
                f"Subtotal: {order.subtotal} \n"
                f"service fee: {order.service_fee} \n"
                f"shipping fee: {order.shipping_fee} \n\n"
                f"Total Payble: {order.payable} \n\n"
                f"----------------------------\n\n"
                f"Shipping Address:\n\n"
                f"Name: {order.full_name}\n"
                f"Address: {order.address_line_1}\n"
                f"Landmark: {order.address_line_2}\n"
                f"State: {order.state}\n"
                f"District: {order.district}\n"
                f"City: {order.city}\n"
                f"Pincode: {order.pin_code}\n"
                f"Mobile: {order.mobile_no}\n"
                f"Email: {order.email}\n\n"
                f"Thank you for placing your order with balad. Your order has been confirmed.your order will be delivered in 7 working days.\n\n"
            )

            email = order.email
            subject = "Order Confirmation - balad"
            message = message
            send_mail(
                subject,
                message,
                "secure.gedexo@gmail.com",
                [email, "info@balad.com"],
                fail_silently=False,
            )

            print("email sent successfully")
            cart = Cart(request)
            cart.clear()

        else:
            print("Signature verification failed, please check the secret key")
            order.payment_status = "Failed"
            order.save()
        return render(request, "web/callback.html", {"object": order})
    else:
        print("Razorpay payment failed")
        return redirect("web:payment", pk=order.pk)


class CompleteOrderView(DetailView):
    model = Order
    template_name = "web/complete-order.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_ordered = True
        order.order_status = "Placed"
        order.save()
        products = ""
        total = 0
        counter = 1
        for item in order.get_items():
            products += (
                f"{counter}.{item.product.product.name}- {item.product.unit} "
                f"({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
            )
            total += item.subtotal()
            counter += 1

        # Generate the WhatsApp message
        message = (
            f"============================\n"
            f"Order Confirmed\n"
            f"============================\n\n"
            f"Order ID: {order.order_id}\n"
            f"Order Date: {order.created}\n"
            f"Order Status: Placed\n"
            f"Payment Method: Cash On Delivery\n"
            f"Payment Status: Pending\n"
            f"----------------------------\n"
            f"Products:\n\n"
            f"{products}\n"
            f"----------------------------\n"
            f"Order Summary:\n\n"
            f"Subtotal: {order.subtotal} \n"
            f"Service Fee: {order.service_fee} \n"
            f"Shipping Fee: {order.shipping_fee} \n\n"
            f"Total Payable: {order.payable} \n\n"
            f"----------------------------\n"
            f"Shipping Address:\n\n"
            f"Name: {order.full_name}\n"
            f"Address: {order.address_line_1}\n"
            f"Landmark: {order.address_line_2}\n"
            f"State: {order.state}\n"
            f"District: {order.district}\n"
            f"City: {order.city}\n"
            f"Pincode: {order.pin_code}\n"
            f"Mobile: {order.mobile_no}\n"
            f"Email: {order.email}\n\n"
            f"Thank you for placing your order with balad. "
            f"Your order has been confirmed. Your order will be delivered in 7 working days.\n\n"
        )

        # Encode the message for WhatsApp URL
        encoded_message = urlencode({"text": message})
        whatsapp_number = order.mobile_no  # Customer's mobile number
        whatsapp_url = f"https://wa.me/{whatsapp_number}?{encoded_message}"

        # Optionally, you can log or display the URL for debugging
        print(f"WhatsApp URL: {whatsapp_url}")

        # Clear the cart
        cart = Cart(request)
        cart.clear()

        # Render the confirmation page
        context = {
            "object": order,
            "whatsapp_url": whatsapp_url,  # Include the URL in the context
        }
        return render(request, self.template_name, context)


class UserOrderDetailView(DetailView):
    model = Order
    template_name = "account/order_single.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"my_order": True}


def get_shipping_fee(request):
    district_id = request.GET.get("district", None)
    data = District.objects.get(id=district_id).delivery_charge
    return JsonResponse({"charge": data})


# class MyAccountView(LoginRequiredMixin, TemplateView):
#     template_name = "web/account_dashboard.html"


class MyOrderView(LoginRequiredMixin, View):
    template_name = "web/account_dashboard.html"

    def get(self, request):
        user = self.request.user
        context = {
            "orders": Order.objects.filter(user=user),
        }
        return render(request, self.template_name, context)


class MyOrderDetailsView(LoginRequiredMixin, DetailView):
    template_name = "web/order_details.html"
    model = Order
    context_object_name = "order"


class AutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        results = []
        if query:
            products = Product.objects.filter(name__icontains=query, is_active=True)[
                :10
            ]
            results = [
                {"name": product.name, "url": product.get_absolute_url()}
                for product in products
            ]
        return JsonResponse(results, safe=False)


def custom_404(request, exception):
    return render(request, "web/404.html", status=404)


def error(request):
    context = {}
    return render(request, "web/404.html", context)


def search_product(request):
    return render(request, "web/search.html")


def my_account_orders(request):
    user = request.user
    context = {
        "orders": Order.objects.filter(user=user),
    }
    return render(request, "web/account-orders.html", context)


def category_list(request, slug):
    category = Category.objects.filter(slug=slug).first()
    sub_category = SubCategory.objects.filter(slug=slug).first()
    if WeddingBanner.objects.filter(slug=slug).exists():
        instance = WeddingBanner.objects.filter(slug=slug).last().category
        print("instance", instance)

    sort_option = request.GET.get("sort", "latest")  # Default sorting
    subcategory_id = request.GET.get("subcategory")  # Get selected subcategory

    query = request.GET.get("q", "").strip()
    products = Product.objects.none()  # Default to empty

    if category:
        products = Product.objects.filter(category=category)
        if  products.last():
            tittle = products.last().category.name
        else:
            tittle = str(category)

    elif sub_category:
        products = Product.objects.filter(subcategory=sub_category)
        tittle = products.last().subcategory.name
    elif festival.exists():
        products = festival
        tittle = f"{products.last().category.name} - Wedding"
    # Apply Subcategory Filtering
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)
        tittle = products.last().category.name

    if query:
        print('query=', query)
        products = products.filter(name__icontains=query)

    # Apply Sorting
    if sort_option == "low-to-high":
        products = products.order_by("order")
    elif sort_option == "high-to-low":
        products = products.order_by("-order")
    else:
        products = products.order_by(
            "-id"
        )  # Assuming 'Latest' sorts by newest products

    # Fetch all subcategories for dropdown
    subcategories = (
        SubCategory.objects.filter(category=category)
        if category
        else SubCategory.objects.all()
    )

    context = {
        "products": products,
        "category": category,
        "subcategory": sub_category,
        "subcategories": subcategories,
        "selected_subcategory": int(subcategory_id) if subcategory_id else None,
        "sort_option": sort_option,
        "tittle": tittle,
        "query": query,  
    }

    return render(request, "web/category_products.html", context)


def offer_sale(request):
    custom = Product.objects.filter(is_sale=True)
    query = request.GET.get("q", "")
    if query:
            custom = custom.filter(name__icontains=query)
           
    context = {
        "custom": custom,
    }
    return render(request, "web/offer.html", context)


def get_images_by_color(request, pk):
    color_id = request.GET.get("color_id")
    product = Product.objects.get(pk=pk)

    # Retrieve product images based on color
    images = ProductImage.objects.filter(product=product, color__id=color_id)

    # Return images as a JSON response
    image_urls = [image.image.url for image in images]
    return JsonResponse({"images": image_urls})


def quick_add_modal(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = product.get_sizes()
    colors = product.get_colors()
    sale_price = product.get_sale_price()
    return JsonResponse(
        {
            "name": product.name,
            "image_url": product.image.url,
            "price": str(sale_price),
            "sizes": [
                {"id": size.id, "unit": size.unit, "sale_price": str(size.sale_price)}
                for size in sizes
            ],
            "colors": [
                {"name": color.name, "hex_code": color.hex_code} for color in colors
            ],
        }
    )


def add_to_cart(request):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        # Ensure product_id and size_id are integers
        print("POST data:", request.POST)

        try:
            product_id = int(request.POST.get("product_id"))
            size_id = int(request.POST.get("size_id"))
            quantity = int(request.POST.get("quantity"))
        except (ValueError, TypeError) as e:
            print(f"Error parsing data: {e}")
            return JsonResponse({"error": "Invalid product or size ID"}, status=400)

        # Get the product, if it doesn't exist return 404
        product = get_object_or_404(Product, id=product_id)

        # Add to cart logic here
        cart = Cart.objects.get(user=request.user)  # Assuming user-based cart
        cart_item, created = cart.items.get_or_create(product=product, size_id=size_id)
        cart_item.quantity += quantity
        cart_item.save()

        # Recalculate cart total and count
        cart_count = cart.items.count()
        cart_total = (
            cart.get_total()
        )  # Assuming Cart model has a method to calculate the total

        return JsonResponse({"cart_count": cart_count, "cart_total": cart_total})

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_product_details(request):
    product_id = request.GET.get("product_id")
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            # Return product details as JSON response
            product_data = {
                "id": product.id,
                "name": product.name,
                "image_url": product.image.url,
                "price": product.price,
                "color": product.color,  # Assuming this field exists
                "size": product.size,  # Assuming this field exists
            }
            return JsonResponse({"product": product_data})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
    else:
        return JsonResponse({"error": "Product ID is missing"}, status=400)


class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Prevent exposure of the queryset for unauthenticated users
        if not self.request.user.is_authenticated:
            return SubCategory.objects.none()

        queryset = SubCategory.objects.all()

        # Check if a `category` parameter is forwarded
        category_id = self.forwarded.get("category", None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Optionally filter by search query
        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        return queryset


def wedding_list(request, slug):
    # Get wedding products
    festival_products = Product.objects.filter(
        is_wedding_product=True, category__slug=slug
    )
    # Get the WeddingBanner for the same category
    wedding_banner = WeddingBanner.objects.filter(category__slug=slug).first()
    query = request.get("q","")
    if query:
        festival_products = festival_products.filter(name__icontains=query)
    context = {
        "festival_products": festival_products,
        "wedding_banner": wedding_banner,
    }
    return render(request, "web/wedding.html", context)


def search_product(request):
    return render (request,'web/search.html')
