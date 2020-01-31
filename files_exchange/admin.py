from django.contrib import admin
from .models import *
from django.utils.text import Truncator

admin.site.register(School)
admin.site.register(TypeSchool)
admin.site.register(Promo)
admin.site.register(Subject)
admin.site.register(FileHomework)
admin.site.register(Moderation)
