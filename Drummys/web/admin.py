from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Countries, Download, Levels, Party, Session, Visit

admin.site.register(Download)
admin.site.register(Levels)
admin.site.register(Party)
admin.site.register(Session)
admin.site.register(Visit)
admin.site.register(Countries)
admin.site.register(CustomUser, UserAdmin)
