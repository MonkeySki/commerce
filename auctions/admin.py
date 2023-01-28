from django.contrib import admin
from .models import User, Bid, Listing, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comments)

