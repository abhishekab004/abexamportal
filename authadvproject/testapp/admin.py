from django.contrib import admin
from testapp.models import Contact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display=['name', 'email', 'subject', 'message']
    
admin.site.register(Contact, ContactAdmin)
