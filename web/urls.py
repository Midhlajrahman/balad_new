from django.urls import path
from django.views.generic import TemplateView
from .views import  get_images_by_color,quick_add_modal,SubCategoryAutocomplete
from . import views


app_name = "web"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="web/privacy_policy.html"),
        name="privacy_policy",
    ),
    path(
        "terms-conditions/",
        TemplateView.as_view(template_name="web/terms_conditions.html"),
        name="terms_conditions",
    ),
    path(
        "refund-policy/",
        TemplateView.as_view(template_name="web/refund_policy.html"),
        name="refund_policy",
    ),
    path(
        "shipping-policy/",
        TemplateView.as_view(template_name="web/shipping_policy.html"),
        name="shipping_policy",
    ),
    path(
        "contact-policy/",
        TemplateView.as_view(template_name="web/contact_policy.html"),
        name="contact_policy",
    ),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path(
        "product-detail/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("whatsapp-order/", views.order, name="order"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("get_shipping_fee/", views.get_shipping_fee, name="get_shipping_fee"),
    path("shop/cart/", views.cart_view, name="cart"),
    path("shop/cart/add/", views.cart_add, name="add_cart"),
    # path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path(
        "shop/cart-item-clear/<str:item_id>/",
        views.clear_cart_item,
        name="clear_cart_item",
    ),
    path("shop/cart-minus/", views.minus_to_cart, name="minus_to_cart"),
    path("shop/cart-clear/", views.clear_cart, name="clear_cart"),
    # payment
    path("payment/<str:pk>/", views.PaymentView.as_view(), name="payment"),
    path("callback/<str:pk>/", views.callback, name="callback"),
    path(
        "complete-order/<str:pk>/",
        views.CompleteOrderView.as_view(),
        name="complete_order",
    ),
    path(
        "user/order/<str:order_id>/detail/",
        views.UserOrderDetailView.as_view(),
        name="order_detail",
    ),
    # path('my-account/',views.MyAccountView.as_view() ,name='my-account'),
    path("my-orders/", views.MyOrderView.as_view(), name="my_orders"),
    # path('order-details/<int:pk>/',views.MyOrderDetailsView.as_view() ,name='order_detail'),
    path(
        "search-autocomplete/",
        views.AutocompleteView.as_view(),
        name="search-autocomplete",
    ),
    path("error/", views.error, name="error"),
    path("product/search/",views.search_product,name='search'),
    path("account/my-orders-list/",views.my_account_orders,name='my_account_orders'),
    path("category/<slug:slug>/",views.category_list,name='category_product'),
    path('product/<int:pk>/images/', get_images_by_color, name='product_images_by_color'),
    path('quick-add/<int:product_id>/', quick_add_modal, name='quick_add_modal'),
    path('get-product-details/', views.get_product_details, name='get_product_details'),
    path('offer_sale/', views.offer_sale, name='offer_sale'),
   

    path('subcategory-autocomplete/', SubCategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
    path("wedding/<slug:slug>/",views.wedding_list,name='wedding'),
 
    
]
