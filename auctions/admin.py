from django.contrib import admin
from .models import User,Listing,Catagory,user_watchList,bids,comments
# Register your models here.
admin.site.register(user_watchList)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Catagory)
admin.site.register(bids)
admin.site.register(comments)                 
