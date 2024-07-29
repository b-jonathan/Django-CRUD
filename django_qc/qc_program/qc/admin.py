#!C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe
from django.contrib import admin
from .models import Complain,ComplainDetails
# Register your models here.

class ComplainAdmin(admin.ModelAdmin):
    list_display = ("complain_type","customer_id","nomor_document",)

admin.site.register(Complain, ComplainAdmin)

class ComplainDetailsAdmin(admin.ModelAdmin):
    list_display = ("complain_id","product_id","status",)


admin.site.register(ComplainDetails, ComplainDetailsAdmin)
