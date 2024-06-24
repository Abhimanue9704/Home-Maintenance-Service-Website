from django.contrib import admin

# Register your models here.
from .models import ServiceProvider,Client,NewUser,fileUpload,Section,serviceList,customerList,booked

admin.site.register(Client)
admin.site.register(ServiceProvider)
admin.site.register(NewUser)
admin.site.register(fileUpload)
admin.site.register(Section)
admin.site.register(serviceList)
admin.site.register(customerList)
admin.site.register(booked)


