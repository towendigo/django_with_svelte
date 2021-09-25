# Django with Svelte

The purpose of this project is to use modern JS front-end frameworks (specifically **Svelte**) with **Django**. 

There are solutions already like django-svelte, which is functioning well. But it is a strongly opinionated solution and lacks flexibility. Also, with that highly opinionated solution, it's reducing what Svelte does best: creating elegant HTML natively and fast, no virtual dom, no wrapper mess.

My goals with this project are:
* Highly flexible setup
* Clean and elegant HTML output such as: 
    * Wrappers are optional but not preferred as Svelte target
    * Declaring data, script and style tags in head, where they belong (Declerations inside body or wrappers are optional but not preferred)
*  Supporting many Svelte compilers with different configurations
* Highly modular and configurable in development state
* Highly modular and configurable in deployment state with minimum alteration necessary





## Setting up the environment :
----
-  **You need:**
    - **Python (3.7+)** -> pip and virtual python enviroment manager (I use virtualenv for that)
    - **Node** -> npm and npx + git

----

1. Create a folder as our working directory. (I named it **working_dir** for it to be clear but you can name it as you want)

Django: 

2. Create a python virtual environment as a folder inside working directory. That's going to be our deployment folder. (I named it **py_venv** for it to be clear but you can name it as you want)

3. Activate python virtual environment. (**py_venv** in this case)

4. Check if python and pip works. (```python --version``` (for python) & ```pip --version``` (for pip))

5. Install Django (3+) and Pillow (optional for image manipulation) with pip in python virtual environment. (```pip install Django``` & ```pip install Pillow```)

6. Start Django project inside python virtual environment. Use ```django-admin startproject django_project```. (I named it **django_project** for it to be clear but you can name it as you want)

7. Create a folder for static files inside python virtual environment (I named it **static** for it to be clear but you can name it as you want)

8. Create a folder for app files inside static folder. (I named it **apps** for it to be clear but you can name it as you want)

9. Create a folder for media files inside static folder.  (I named it **media** for it to be clear but you can name it as you want)

If everything is good we are done with pythonic (Django) part right now. Next step is setting up svelte compilers.

Svelte:

10. Create another terminal for Svelte without deactivating python virtual environment. (We are going to use it later)

11. Create a folder for svelte compilers in working directory. (I named it **svelte_compilers** for it to be clear but you can name it as you want)

12. Check if node and npm/npx works. (```node -v``` (for node) & ```npm -v``` (for npm) & ```npx -v``` (for npx))

13. Check if git works. Use ```git version```. 

If git is not installed on your system, install git and continue with step 14 or download the svelte-template from https://svelte.dev/blog/the-easiest-way-to-get-started and unzip it into a folder inside svelte compilers. We are going to use this as a svelte compiler template. (I named it **svelte_template** for it to be clear but you can name it as you want). If you unzipped the template manually you can skip step 14.  

14. Inside svelte compilers setup a svelte-template. Use ```npx degit sveltejs/template svelte_template```. We are going to use this as a svelte compiler template. (I named it **svelte_template** for it to be clear but you can name it as you want with changing svelte_template part)

15. Inside svelte-template run ```npm install```.

If everything is good we are done with svelte part too. So setup is over.


## Configuration :

### Svelte/rollup configuration:
Find **rollup.config.js** file inside svelte-template. We are going to make some changes in this file for svelte part to work. 

Ideally we want our static files and svelte compilers modular and usually we use directories to logically structure our files. Ideally we want our static app files and svelte compilers to share same logic in structure. For example:
    
    svelte_compilers
    |---- ...
    |---- svelte_template
    |       |---- ...
    |       |---- ...
    |       |---- ...
    |       |---- rollup.config.js
    |
    |---- some_compiler
            |---- ...
            |---- ...
            |---- ...
            |---- rollup.config.js
    __________________________________
    static
    |---- media
    |       |---- ...
    |       
    |---- apps
            |---- svelte_template
            |       |---- bundle.js
            |       |---- bundle.js.map
            |       |---- bundle.css
            |
            |---- some_compiler
                    |---- bundle.js
                    |---- bundle.js.map
                    |---- bundle.css        

We want svelte-template to be automated so we need a automated way of handling output paths. 

Add this part to **rollup.config.js** right after imports:

``` js
const path = require('path'); // add path module
const cur_path = (require.main.path).split(path.sep); // create an array of the main file's (rollup.config.js) path
const appbase = cur_path[cur_path.length-5]; // get the 5. element from last of array (thats the name of our compiler because this code executes at somewhere else)
const static_path = '../../py_venv/static/apps'; // relative path of our static folder
const appname = static_path + appbase + '/bundle.js'; // create app name relative to the compiler
```

Change this part:
``` js
export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	}
    
// as

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: appname //dynamic app name
	}
```
We are done with svelte/rollup configuration. After that you can just copy and paste the svelte-template and rename it as you want (for example hello world).

If your static folder path is different, change it on static_path in **rollup.config.js**.

If you want your output js file's name different than bundle.js change it on appname in **rollup.config.js**. 

And if you want your output css file's name different than bundle.css change it on **rollup.config.js** with:

``` js 
css({ output: 'bundle.css' }), 

// as

css({ output: 'WhatYouWant.css' }),
```

----

Note: You can change the logical structures of static files and svelte compilers as you have already learned how to automate it.

----

### Django configuration:

We are going to change django **settings.py** because we want a way to serve static files (js, css, media etc.). Django can do that for us in development state but that's really unefficient. Hopefully in production **Apache** or **Ngnix** is going to do that for us. That's why we want our static files in a single folder and we want them to be logically structured. But for now, let's change settings.py.

---
In **settings.py** find this line: 
``` python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
```
I am not going to change anything on that. 
That's our static url. If we want a css file named istanbul.css we are going to link it as "...root/**static/istanbul.css**". You can change that if you want.

----

In **settings.py** add this code to somewhere in the middle:
```python
# Static file directories (in this case static folder in py_venv)
STATICFILES_DIRS = [
    ("media", BASE_DIR.parent / "static/media"), # adding media folder as a static file directory with the name of media
    ("apps", BASE_DIR.parent / "static/apps"), # adding apps folder as a static file directory with the name of apps
]
```

Now django knows wich static directories we want to use. Also django is clever enough to understand the full path when we use just media or apps. That prevents long links. 

You can name paths as you want with changing media or apps with something else or add a new path. Just remember, better practice is naming paths understandably.  

----

Note: If you have a different logical structure of static files, you should change the staticfiles directories respectedly as you have already learned how to do it.

----


We are done with django configuration. Next we are going to try hello world with django and svelte.


## Hello World App :

In this section i am going to create a hello world app with django and svelte. The app is going to respond get requests with a nice hello world in different languages. We are going to extract language from url and store the translations of "hello world" at database.

### Django part:

First lets create a django app named hello_world. If your terminal is closed, activate your python virtual environment, change directory into django_project and create an app like that: (I am using virtualenv and cmd as a terminal so you might need to alter it for your terminal and virtual environment manager) 

```cmd
:: activate python virtual environment &
Scripts\activate &
:: change directory into django_project &
cd django_project &
:: create hello_world app &
python manage.py startapp hello_world
```
You can name your app as you want. But i am going to make a hello world app in this step.

Now we have an app named hello world. Find **settings.py** and add our app into the end of installed apps. Like that:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello_world', # app name
]
```
If your app has a different name use it instead of hello world

Than find **django_project/django_project/urls.py** and change it like that:
```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# as 

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello_world/', include("hello_world.urls")),# directing root/hello_world route to hello_world app
]
```

Go to hello_world app folder and create an urls.py file. Copy paste this:
```python
from django.urls import path

urlpatterns = [
   
]
```
Create a folder named templates inside your apps folder. Create a folder in your app's name inside this templates folder. Inside this folder create a file named **hello_world.html** (You can name the template as you want).

It is going to look like that:

    |---- hello_world (or your app's name)
            |---- templates
            |       |---- hello_world (or your app's name)
            |              |---- hello_world.html (or your template's name)
            |      
            |---- ...


There is a reason for us to do it like that. Django looks for templates inside apps if we don't specify not to. But it gets the first match and renders that. So we want a way to differ between templates inside different apps even if their names are same. 

Now that we have a template, we need a view. Go to your app/views.py and lets create a function based view. Like that:

```python
from django.shortcuts import render
# Create your views here.

# returns hello world template without lan
def hello_world(request):
    return render(request, "hello_world/hello_world.html")

# returns hello world template
def hello_world_lan(request, lan):
    return render(request, "hello_world/hello_world.html")
```
That is the simplest form of views plus it does nothing. We are going to change it in a minute or so but we need our model for languages now.

Go to your app/models.py (in this case hello_world/models.py) and create a model like this:

```python
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
```

We have two models. One for colors for languages and other for hello world.

Now lets register the model for admin, go to your app/admin.py (in this case hello_world/admin.py) and register the model like this: 

```python
from django.contrib import admin
from .models import HelloWorld, LanguageColors
# Register your models here.

admin.site.register([LanguageColors, HelloWorld])
```
We have a HelloWorld model now. We are going to populate it with admin site. We need to create a super user and apply changes. (I choose admn as username - Dj4ngo_w1th_svelt3 as password - blank email) 

---
Not: Never share this data !

---

```cmd
:: inside django_project directory &
python manage.py makemigrations &
python manage.py migrate &
python manage.py createsuperuser &
:: choose username, email, password - never share this data &
python manage.py runserver 
```

Now django should give you some output like this:

    Django version 3.2.7, using settings 'django_project.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.

Go to ` http://127.0.0.1:8000/admin ` and log in as super user.

Add language colors and than hello worlds for all languages: 

(You need 3 hex color values for language colors. You can pick colors from flags of the biggest/oldest countries in which language is spoken. And you need translation of "Hello World" for every languages) 

![Image of Admin Panel](https://github.com/towendigo/django_with_svelte/blob/master/images/Admin.PNG)
![Image of Language Color Object](https://github.com/towendigo/django_with_svelte/blob/master/images/LanguageColor.PNG)
![Image of Hello World Object](https://github.com/towendigo/django_with_svelte/blob/master/images/helloworld.PNG)

If everything is good we are done with models.

Go back to your app/urls.py (in our case hello_world/urls.py) change it like that:

```python
from django.urls import path

urlpatterns = [
   
] 

# as 

from django.urls import path
from .views import hello_world, hello_world_lan

urlpatterns = [
   path("", hello_world, name="hello_world"), # default without language specified
   path("<str:lan>", hello_world_lan, name="hello_world_lan"), # get language from url 
]
```

Now go to the your app/views.py (hello_world/views.py) and change it like that:

```python
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
```

Now there is just our template left with pythonic part of this section. Go to your app/templates/your app/your template (hello_world\templates\hello_world\hello_world.html) and copy paste this: 

```html
{% load static %} {# load static directories #}

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset='utf-8'>
	<meta name='viewport' content='width=device-width,initial-scale=1'>

	<title>
        {% autoescape on %}
           {{values.content.content}} {# Get hello world as title + sanitize #}
        {% endautoescape %}
    </title>
	
    {# If your svelte compiler's name is different, use it instead of hello_world : #}

	<link rel='stylesheet' href=" {% static 'apps/hello_world/bundle.css' %} "> {# Get hello_world svelte output for css #}

	{{ values|json_script:"values-json"}} {# Insert data (values) as json with id="values-json" #}

	<script defer src=" {% static 'apps/hello_world//bundle.js' %} "></script> {# Get hello_world svelte output for js #}
	
    <style> 
        *{ 
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
    </style> {# just simple global styling #}
</head>

<body>
</body>

</html>
```

We are done with django now. Check if every thing works with running django server. If everyhting is good do not kill the server. 

### Svelte part:

Copy our svelte template inside svelte compilers and paste it as a sibling. Rename it as hello_world (you can name it as you want but change the path for output files in your django template respectedly.)

It should look like that:

    |---- svelte_compilers
            |---- svelte_template
            |       |---- ...
            |       |---- ...
            |      
            |---- hello_world  (or your compiler's name)
                    |---- ...
                    |---- ...

Now let's start our svelte compiler. Open a terminal and change directory as hello_world (or your compiler's name). Run :

```cmd
:: run compiler as development stage &
npm run dev 
```

Now we have our compiler running and ready. Go to src folder inside compiler and open **`main.js`**. Change it like that:

```js
import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'world'
	}
});

export default app;

// as

import App from './App.svelte';

const app = new App({
	target: document.body, // our target is body directly instead of wrapper elements
    // we dont need any props for this project
});

export default app;
```

In src folder create a file named **`language.js`** (you can name it as you want). And copy paste this:

```js
import { readable } from 'svelte/store';

// get data from django-template
export const lanJS = readable(JSON.parse(document.getElementById("values-json").textContent));
```

In src folder open **`App.svelte`**. Change it like that:

```html
<script>
	import {lanJS} from './language'; // our data from django-template
	
	// parsing data
	let content = $lanJS.content.content;  // dollar sign is used to subscribe to store (our data from django-template)
	let colors = $lanJS.color;
	let message = $lanJS.message;
	// ------
</script>

<main>
	<h1>
		{content} <!-- hello world -->
		<span style="color:{colors.color1};"> ! </span> <!-- ! sign in color1 -->
		<span style="color:{colors.color2};"> ! </span> <!-- ! sign in color2 -->
		<span style="color:{colors.color3};"> ! </span> <!-- ! sign in color3 -->
	</h1> 

	{#if message} <!-- if there is a (warning) message show message in footer -->
	<footer>
		<p>
			{message} <!-- (warning) message -->
		</p>
	</footer>
	{/if}
</main>

<style> /* Styling */
	main{
		height: 100vh;
		width: 100vw;

		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;

		color: white;
		text-align: center;

		background-image: url("http://127.0.0.1:8000/static/media/worldmap.svg");
		background-repeat: no-repeat;
		background-size: contain;
		background-position: center;
	}
	h1{
		padding: 1em 2em;
		width: fit-content;
		
		background: #00000099;
		box-shadow: 0px 0px 1em 0.5em #00000099;
	}
	footer{
		position: absolute;
		bottom: 0px;
		left: 0px;
		width: 100%;
		height: fit-content;
		padding: 1em 2em;

		background: #00000099;
	}
</style>
```

If there is no problem, kill your svelte compiler (Ctrl-C). And run:

```cmd
:: run compiler as build stage &
npm run build
```

Our hello-world app is done. 