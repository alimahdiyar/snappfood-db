from django.contrib import admin

# Register your models here.
from snappfood.models import Comment, Invoice, Discount, Wallet, Cart, User, Food, Category, Admin, Shop, Address, City

admin.site.register(City)
admin.site.register(Address)
admin.site.register(Shop)
admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Wallet)
admin.site.register(Discount)
admin.site.register(Invoice)
admin.site.register(Comment)
