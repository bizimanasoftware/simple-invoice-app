from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
import uuid

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, username, pin, **extra_fields):
        """
        Create and save a User with the given username and pin.
        """
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(pin) # The pin is handled like a password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, pin, **extra_fields):
        """
        Create and save a SuperUser with the given username and pin.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, pin, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with a username and a 4-digit PIN.
    """
    username = models.CharField(max_length=150, unique=True)
    pin_validator = RegexValidator(regex=r'^\d{4}$', message='PIN must be 4 digits.')
    # The pin is stored in the 'password' field of AbstractBaseUser, which handles hashing.
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['pin']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Product(models.Model):
    """
    Represents a product, item, or service.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Client(models.Model):
    """
    Represents a client for whom a receipt is generated.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Receipt(models.Model):
    """
    Represents a generated receipt.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    seller_name = models.CharField(max_length=200, default="My Business")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Receipt {self.id} for {self.user.username}"

class ReceiptItem(models.Model):
    """
    Represents an item within a receipt.
    """
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.product_name
