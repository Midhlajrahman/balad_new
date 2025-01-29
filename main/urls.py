from django.urls import path

from . import views
from .views import LoadSubcategoriesView
app_name = "main"

urlpatterns = [
    path("dashboard/", views.IndexView.as_view(), name="index"),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path(
        "order/<str:order_id>/detail/",
        views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "invoice/<str:order_id>/",
        views.InvoiceView.as_view(),
        name="invoice",
    ),
    path("order/update/", views.OrderUpdateView.as_view(), name="order_update"),
    # catgory
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/<str:pk>/update/",
        views.CategoryUpdate.as_view(),
        name="category_update",
    ),
    path(
        "category/<str:pk>/delete/",
        views.CategoryDelete.as_view(),
        name="category_delete",
    ),
    # product
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("product/create/", views.CreateProductView.as_view(), name="product_create"),
    path("product/<pk>/edit/", views.edit_product, name="product_update"),
    path(
        "product/<str:pk>/delete/", views.ProductDelete.as_view(), name="product_delete"
    ),
    # reviews
    path("reviews/", views.ReviewListView.as_view(), name="review_list"),
    path("review/create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("review/<pk>/edit/", views.ReviewUpdateView.as_view(), name="review_update"),
    path(
        "review/<str:pk>/delete/",
        views.ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    # state
    path("states/", views.StateListView.as_view(), name="states"),
    path("state/create/", views.StateCreateView.as_view(), name="state_create"),
    path(
        "state/<str:pk>/update/", views.StateUpdateView.as_view(), name="state_update"
    ),
    path(
        "state/<str:pk>/delete/", views.StateDeleteView.as_view(), name="state_delete"
    ),
    # district
    path("districts/", views.DistrictListView.as_view(), name="districts"),
    path(
        "district/create/", views.DistrictCreateView.as_view(), name="district_create"
    ),
    path(
        "district/<str:pk>/update/",
        views.DistrictUpdateView.as_view(),
        name="district_update",
    ),
    path(
        "district/<str:pk>/delete/",
        views.DistrictDeleteView.as_view(),
        name="district_delete",
    ),
    # customer
    path("customers/", views.CustomerListView.as_view(), name="customers"),
     # sliders
    path("sliders/", views.SliderListView.as_view(), name="sliders"),

    path(
        "slider/create/", views.SliderCreateView.as_view(), name="slider_create"
    ),
    path(
        "slider/<str:pk>/update/",
        views.SliderUpdateView.as_view(),
        name="slider_update",
    ),
    path(
        "slider/<str:pk>/delete/",
        views.SliderDeleteView.as_view(),
        name="slider_delete",
    ),
    # Shipping Fee
    path("shippingfees/", views.ShippingListView.as_view(), name="shippingfees"),
    path("shippingfee/create/", views.ShippingCreateView.as_view(), name="shippingfee_create"),
    path("shippingfee/<str:pk>/update/", views.ShippingUpdateView.as_view(), name="shippingfee_update"),
    path("shippingfee/<str:pk>/delete/", views.ShippingDeleteView.as_view(), name="shippingfee_delete"),
    
    # Contact
    path("contact/", views.ContactListView.as_view(), name="contacts"),
    path("contact/<str:pk>/delete/", views.ContactDeleteView.as_view(), name="contact_delete"),
    path("contact/<str:pk>/update/", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contact/create/", views.ContactCreateView.as_view(), name="contact_create"),
    
    #testimonial
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonials"),
    path("testimonial/create/", views.TestimonialCreateView.as_view(), name="testimonial_create"),
    path("testimonial/<str:pk>/update/", views.TestimonialUpdateView.as_view(), name="testimonial_update"),
    path("testimonial/<str:pk>/delete/", views.TestimonialDeleteView.as_view(), name="testimonial_delete"),

    #subcategory
      # catgory
    path("subcategories/", views.SubCategoryListView.as_view(), name="sub_categories"),
    path(
        "subcategory/create/", views.SubCategoryCreateView.as_view(), name="sub_category_create"
    ),
    path(
        "subcategory/<str:pk>/update/",
        views.SubCategoryUpdate.as_view(),
        name="sub_category_update",
    ),
    path(
        "subcategory/<str:pk>/delete/",
        views.SubCategoryDelete.as_view(),
        name="sub_category_delete",
    ),

       # wedding
    path("wedding/", views.WeddingListView.as_view(), name="wedding"),

    path(
        "wedding/create/", views.WeddingCreateView.as_view(), name="wedding_create"
    ),
    path(
        "wedding/<str:pk>/update/",
        views.WeddingUpdateView.as_view(),
        name="wedding_update",
    ),
    path(
        "wedding/<str:pk>/delete/",
        views.WeddingDeleteView.as_view(),
        name="wedding_delete",
    ),
           # Brands
    path("brands/", views.BrandsListView.as_view(), name="brands"),

    path(
        "brands/create/", views.BrandsCreateView.as_view(), name="brands_create"
    ),
    path(
        "brands/<str:pk>/update/",
        views.BrandsUpdateView.as_view(),
        name="brands_update",
    ),
    path(
        "brands/<str:pk>/delete/",
        views.BrandsDeleteView.as_view(),
        name="brands_delete",
    ),
    path("load-subcategories/", LoadSubcategoriesView.as_view(), name="load_subcategories"),
    
]
