from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class BusinessProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, blank=False)
    phone = PhoneNumberField(region='US')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    # slug = unknown yet/ need research to create unique identifier for a shareable URL
    #models.SlugField max_length and unique
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        """Custom validation to ensure slug is not empty."""
        if not self.slug:
            self.slug = slugify(self.business_name)
        if not self.slug:
            raise ValidationError("Slug cannot be empty.")

    def has_duplicate_slug(self):
        return self.__class__.objects.filter(slug=self.slug).exclude(pk=self.pk).exists()
    
    def make_unique_slug(self):
        base_slug = self.slug
        candidate = base_slug
        counter = 2

        while self.__class__.objects.filter(
            slug=candidate
        ).exclude(pk=self.pk).exists():
            candidate = f"{base_slug}-{counter}"
            counter += 1

        self.slug = candidate
        
    # def duplicate_slug(self):
    #     counter = 2
    #     while BusinessProfile.objects.filter(slug=slug).exists():
    #         slug = f"{self.slug}-{counter}"
    #         counter += 1
    #     self.slug = slug
     
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.business_name)
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.business_name

class Service(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=False)
    description = models.TextField(max_length=500, blank=True)
    base_price = models.DecimalField(blank=False, default=0, max_digits=6, decimal_places=2, validators=[
        MinValueValidator(0)
    ])
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
            return self.name
     