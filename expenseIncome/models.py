from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


from decimal import Decimal


# Create your models here.

class Expense(models.Model):

    TRANSACTION_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit')
    )

    TAX_TYPE_CHOICES = (
        ('flat', 'Flat'),
        ('percentage', 'Percentage')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
                       max_length=10, choices=TRANSACTION_CHOICES
                    )
    tax = models.DecimalField(default=Decimal('0.00'), 
                              validators= [MinValueValidator(Decimal('0.00'))], max_digits=10, 
                              decimal_places=2
                              )
    tax_type = models.CharField(max_length=15, choices=TAX_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'{self.title} by {self.user.username}  latest updated at {self.updated_at}'
    
    class Meta:
        ordering = ['-created_at']

    @property
    def total(self):
        if self.tax_type == 'flat':
            return self.amount + self.tax
        elif self.tax_type == 'percentage':
            return self.amount * (1 + self.tax/100)
        else:
            return self.amount
