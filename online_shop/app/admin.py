from django.contrib import admin
from .models import Product, Category, Comment, Message, LikedProduct, ViewedProduct, UserProfile
# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(LikedProduct)
admin.site.register(ViewedProduct)
admin.site.register(UserProfile)
