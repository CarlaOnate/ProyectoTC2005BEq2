from django.contrib import admin

# Register your models here.
from .models import User, Countries, Download, Levels, Party, Session, Visit

admin.site.register(User);
admin.site.register(Countries);
admin.site.register(Download);
admin.site.register(Levels);
admin.site.register(Party);
admin.site.register(Session);
admin.site.register(Visit);
