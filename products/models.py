from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User
from main.models import COLOR_CHOICES, UNIT_CHOICES
import webcolors

class Slider(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to="slider/")
    mobile_image = models.ImageField(upload_to="slider/",blank=True,null=True)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")
        ordering = ("title",)
    
    def get_list_url():
        return reverse_lazy("main:sliders")
    
    def get_update_url(self):
        return reverse_lazy("main:slider_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:slider_delete", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    image = VersatileImageField(
        "category",
        blank=True,
        null=True,
        upload_to="categories/",
        help_text=" The recommended size is 120x120 pixels.",
    )
    status = models.CharField(
        max_length=20,
        choices=(("Published", "Published"), ("Unpublished", "Unpublished")),
        default="Published",
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)

    def get_products(self):
        return Product.objects.filter(category=self)

    def get_product_count(self):
        return self.category.count()
    
    def get_subcategories(self):
        return SubCategory.objects.filter(category=self)
    
    def get_absolute_url(self):
        return reverse_lazy("web:category_product", kwargs={"slug": self.slug})


    def __str__(self):
        return f"{self.name}"
    
class Brands(models.Model):
    brand_name = models.CharField(max_length=50)
    brand_image = models.ImageField(upload_to="Brands")

    def __str__(self):
        return self.brand_name
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
       

class FestivalSeason(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="festivalseasion"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    banner_image = VersatileImageField(
        "subcategory",
        blank=True,
        null=True,
        upload_to="subcategories/season",
        help_text="The recommended size is 120x120 pixels.",
    )
    status = models.CharField(
        max_length=20,
        choices=(("Published", "Published"), ("Unpublished", "Unpublished")),
        default="Published",
    )

    class Meta:
        verbose_name = _("Festival Season")
        verbose_name_plural = _("Festival Season")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy("web:category_product", kwargs={"slug": self.slug})
    

    
       
class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = VersatileImageField(
        "subcategory",
        blank=True,
        null=True,
        upload_to="subcategories/",
        help_text="The recommended size is 120x120 pixels.",
    )
    status = models.CharField(
        max_length=20,
        choices=(("Published", "Published"), ("Unpublished", "Unpublished")),
        default="Published",
    )
    is_display_sub_category=models.BooleanField(default=False)

    class Meta:
        verbose_name = _("SubCategory")
        verbose_name_plural = _("SubCategories")
        ordering = ("name",)
        unique_together = ("category", "slug")

    def get_products(self):
        return Product.objects.filter(subcategory=self)

    def __str__(self):
        return f"{self.category}-{self.name}"
    
    def get_absolute_url(self):
        return reverse_lazy("web:category_product", kwargs={"slug": self.slug})
    
class Product(models.Model):
    order = models.IntegerField(unique=True, blank=True,null=True)
    category = models.ForeignKey(
        "products.Category", on_delete=models.CASCADE, related_name="category"
    )
    subcategory = models.ForeignKey(
        "products.SubCategory", on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )
    brands = models.ForeignKey(
        "products.Brands", on_delete=models.CASCADE, related_name="brands", null=True, blank=True
    )
    is_customisable = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=100,null=True,blank=True,unique=True)
    details = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="products/", help_text=" The recommended size is 450x600 pixels."
    )
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_sale = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)

    # meta
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)

    class Meta:
        ordering = [
            "order",
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    # def save(self, *args, **kwargs):
    #     if not self.image.name:
    #         unique_filename = f"kmtsilks_{self.slug}_{uuid.uuid4()}.webp"
    #         self.image.name = os.path.join( unique_filename)
    #         super(Product, self).save(*args, **kwargs)

    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_image(self):
        return ProductImage.objects.filter(product=self).first()

    def get_sizes(self):
        return AvailableSize.objects.filter(product=self, is_stock=True)

    def get_sale_price(self):
        return min([p.sale_price for p in self.get_sizes()])

    def get_regular_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.regular_price for p in sizes if p.regular_price is not None]
        return min(valid_prices) if valid_prices else None

    def get_offer_percent_first(self):
        return self.get_sizes().first().offer_percent()

    def get_offer_percent(self):
        return min([p.offer_percent() for p in self.get_sizes()])

    def related_products(self):
        return Product.objects.filter().exclude(pk=self.pk).distinct()[0:12]

    def get_absolute_url(self):
        return reverse_lazy("web:product_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse_lazy("main:product_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:product_delete", kwargs={"pk": self.pk})

    def get_reviews(self):
        return Review.objects.filter(product=self, approval=True)

    def num_of_reviews(self):
        return self.get_reviews().count()
    
    def get_weight(self):
        # Retrieve the first AvailableSize instance with stock for the product
        available_size = AvailableSize.objects.filter(product=self, is_stock=True).first()
        return available_size.weight if available_size else None
    
    def get_images_by_color(self, color_name):
        return self.images.filter(color__name=color_name)

   
    def __str__(self):
        return f" {self.name}"
    
    def get_sizes(self):
        return self.sizes.all()

    def get_colors(self):
        return self.colour_set.all()


class Colour(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colour_set',)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/color')
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            self.hex_code = webcolors.name_to_hex(self.name.lower())
        except ValueError:
            self.hex_code = '#FFFFFF'  # Default to white if the name is not valid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/", help_text=" The recommended size is 800x600 pixels."
    )
    color = models.ForeignKey(
        Colour, on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ("product",)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ProductImage, self).delete(*args, **kwargs)
        storage.delete(path)



class AvailableSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='sizes' )
    # size = models.IntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    regular_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    
    is_stock = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Available Size")
        verbose_name_plural = _("Available Sizes")
        ordering = ("sale_price",)

    def offer_percent(self):
        if self.regular_price and self.regular_price != self.sale_price:
            return ((self.regular_price - self.sale_price) / self.regular_price) * 100
        return 0

    # def save(self, *args, **kwargs):
    #     if self.regular_price is None:
    #         self.regular_price = self.sale_price
    #         super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("web:offer_details", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.product} - {self.unit} "
    

    def get_sale_price(self):
        return self.sale_price

class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    fullname = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name}"


