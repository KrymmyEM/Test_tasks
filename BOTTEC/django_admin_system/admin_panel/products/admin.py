from django.contrib import admin
from .models import Categories, Sub_Categories, Items

# Register your models here.:with 
admin.site.register(Categories)
admin.site.register(Sub_Categories)
admin.site.register(Items)
