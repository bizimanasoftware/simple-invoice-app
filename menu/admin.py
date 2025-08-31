from django.contrib import admin
from .models import CustomUser, Product, Client, Receipt, ReceiptItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Receipt)
admin.site.register(ReceiptItem)
