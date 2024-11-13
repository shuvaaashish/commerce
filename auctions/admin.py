from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Watchlist)



