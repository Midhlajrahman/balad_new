from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse_lazy

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(
        max_length=15,
    )
    subject = models.CharField(
        max_length=120,
    )
    message = models.TextField()
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def get_list_url():
        return reverse_lazy("main:contacts")

    def get_update_url(self):
        return reverse_lazy("main:contact_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:contact_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=120)
    description = models.TextField()
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def get_list_url():
        return reverse_lazy("main:testimonials")

    def get_update_url(self):
        return reverse_lazy("main:testimonial_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:testimonial_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)


class CustomOrder(models.Model):
    product_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    front_neck_depth = models.DecimalField(max_digits=5, decimal_places=2)
    back_neck_depth = models.DecimalField(max_digits=5, decimal_places=2)
    bust = models.DecimalField(max_digits=5, decimal_places=2)
    waist = models.DecimalField(max_digits=5, decimal_places=2)
    sleeve_length = models.DecimalField(max_digits=5, decimal_places=2)
    shoulder_length = models.DecimalField(max_digits=5, decimal_places=2)
    full_length = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=170, blank=True, null=True)
    meta_keywords = models.CharField(max_length=170, blank=True, null=True)
    meta_description = models.CharField(max_length=170, blank=True, null=True)
    auther = models.CharField(max_length=100, default="Admin")   
    date = models.DateField()
    image = models.ImageField(upload_to='blog/')
    description = HTMLField()
    
    def get_absolute_url(self):
        return reverse_lazy("web:blog_detail", kwargs={"slug": self.slug})
    
    def get_list_url():
        return reverse_lazy("main:blogs")

    def get_update_url(self):
        return reverse_lazy("main:blog_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:blog_delete", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
    