from django.shortcuts import render
from .models import *

# Create your views here.

# returns hello world template without lan
def hello_world(request):
    lan = "en" # default as en
    content = list(HelloWorld.objects.filter(language=lan).values())[0] # helloworld object
    color = list(LanguageColors.objects.filter(language=lan).values())[0] # languagecolor object
    message = "Language code isn't specified. Redirected to English." # message
    arg = {'content': content, 'color': color, 'message': message} # objects combined

    return render(request, "hello_world/hello_world.html", {'values': arg}) # we are passing argument with a key called 'values' because we are going to reference it later in template

# returns hello world template
def hello_world_lan(request, lan):

    lan_list = [language[0] for language in HelloWorld.LANGUAGES]
    message = 0 # message default as false (0)
    if not lan or lan not in lan_list:
        message = "'%s' is not a valid language code. Redirected to English." %lan # message
        lan = "en" # default as en if not valid

    content = list(HelloWorld.objects.filter(language=lan).values())[0] # helloworld object
    color = list(LanguageColors.objects.filter(language=lan).values())[0] # languagecolor object
    arg = {'content': content, 'color': color, 'message': message} # objects combined
    
    return render(request, "hello_world/hello_world.html", {'values': arg}) # we are passing argument with a key called 'values' because we are going to reference it later in template