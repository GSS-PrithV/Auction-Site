from django.contrib import admin

from .models import User, Listing, Category, Comment, Bids
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "StartingBid", "category")


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(User) 
admin.site.register(Bids)
admin.site.register(Comment)