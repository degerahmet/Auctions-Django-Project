from django.contrib import admin


from .models import Product,User,Category,Comment,Bid
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title","Bid","ImageUrl","description")


admin.site.register(Product,ProductAdmin)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)