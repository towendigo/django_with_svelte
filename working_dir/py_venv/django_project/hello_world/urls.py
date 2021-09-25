from django.urls import path
from .views import hello_world, hello_world_lan

urlpatterns = [
   path("", hello_world, name="hello_world"), # default without language specified
   path("<str:lan>", hello_world_lan, name="hello_world_lan"), # get language from url 
]