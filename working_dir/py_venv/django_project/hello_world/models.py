from django.db import models

# Create your models here.

class LanguageColors(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('tr', 'Turkish'),
        ('de', 'German'), 
        ('es', 'Spanish'), 
        ('fr', 'French'),  
    ]
    language = models.CharField(max_length=2, choices=LANGUAGES, primary_key=True) # choose from LANGUAGES
    color1 = models.CharField(max_length=7) # first flag color for languages
    color2 = models.CharField(max_length=7) # second flag color for languages
    color3 = models.CharField(max_length=7) # third flag color for languages

class HelloWorld(models.Model):
    LANGUAGES = [
        ('en', 'English'), 
        ('tr', 'Turkish'),
        ('de', 'German'), 
        ('es', 'Spanish'), 
        ('fr', 'French'),  
    ]
    language = models.CharField(max_length=2, choices=LANGUAGES, primary_key=True) # choose from LANGUAGES
    content = models.CharField(max_length=200) # translations of hello world