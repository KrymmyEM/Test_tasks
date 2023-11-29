from django.contrib import admin
from .models import Check_Groups, Check_Channels, Users, Maillings, Questions

# Register your models here.:with 

admin.site.register(Check_Groups)
admin.site.register(Check_Channels)
admin.site.register(Users)
admin.site.register(Maillings)
admin.site.register(Questions)
