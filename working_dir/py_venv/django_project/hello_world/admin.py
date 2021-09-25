from django.contrib import admin
from .models import HelloWorld, LanguageColors
# Register your models here.

admin.site.register([LanguageColors, HelloWorld])
