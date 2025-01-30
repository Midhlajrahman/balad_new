from django.conf import settings
from products.models import Category,Product,AvailableSize,SubCategory
from web.cart import Cart
from decimal import Decimal
from django.shortcuts import get_object_or_404

def main_context(request):
    all_categories = Category.objects.all()
    all_sub = SubCategory.objects.all()
    cart_instance = Cart(request)
    cart = cart_instance.cart
    cart_count = len(cart)
    popular_image = None
    query=request.GET.get("q","")
    product = Product.objects.filter(name__icontains=query)
    display_women_sub_category=SubCategory.objects.filter(is_display_sub_category=True,category__name='Women')
    display_men_sub_category=SubCategory.objects.filter(is_display_sub_category=True,category__name='Men')

    cart_items = []
    cart_total = Decimal(0)

    # Calculate cart items and total
    for item_id, item_data in cart.items():
        variant = get_object_or_404(AvailableSize, id=item_id)
        quantity = item_data["quantity"]
        total_price = Decimal(item_data["sale_price"]) * quantity
        cart_items.append({
            "product": variant,
            "quantity": quantity,
            "total_price": total_price,
        })
        cart_total += total_price
    return {
        "all_categories": all_categories,
        "cart_count": cart_count,
        "domain": request.META["HTTP_HOST"],
        "current_version": "?v=2.0",
        "RAZOR_PAY_KEY": settings.RAZOR_PAY_KEY,
        "RAZOR_PAY_SECRET": settings.RAZOR_PAY_SECRET,
        "popular_image": popular_image,
        'search_product':product,
        'query':query,
        "cart_items": cart_items,
        "cart_total": cart_total,
        'all_sub':all_sub,
        'display_women_sub_category': display_women_sub_category,
        'display_men_sub_category':display_men_sub_category
        
    }
