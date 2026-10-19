from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, max_length=15, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=30, blank=False)
    phone = PhoneNumberField(region='US')
    # slug = unknown yet/ need research to create unique identifier for a shareable URL
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user
    
class Service(models.Model):
    # business = should i do foreign key?
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=500, blank=True)
    base_price = models.FloatField(blank=False, default=0)
    is_active = models.BooleanField(default=True)
    pass
    