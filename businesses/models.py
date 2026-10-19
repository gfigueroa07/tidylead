from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, blank=False)
    phone = PhoneNumberField(region='US')
    # slug = unknown yet/ need research to create unique identifier for a shareable URL
    #models.SlugField max_length and unique
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    