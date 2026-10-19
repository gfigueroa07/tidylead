from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from businesses.models import BusinessProfile, Service
# Create your models here.


class QuoteRequest(models.Model):
    lead_status = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('closed', 'Closed')
    ]
    
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField()
    phone = PhoneNumberField(region="US")
    bedrooms = models.PositiveSmallIntegerField(blank=False, max_digits=2, decimal_places=1, validators=[
        MinValueValidator(0)
    ])
    bathrooms = models.DecimalField(blank=False, max_digits=2, decimal_places=1, validators=[
        MinValueValidator(0)
    ])
    customer_message = models.TextField(max_length=500, blank=True)
    estimated_price = models.DecimalField(blank=False)
    status = models.CharField(max_length=20, choices=lead_status, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.customer_name