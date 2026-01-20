# Django

## Installing Django

First, create a virtual environemnt

```bash
python -m venv .venv
```

Then, enter it:

```bash
. .venv/bin/activate
```

Now, you can install django using pip:

```bash
python -m pip install django
```

Chech the installation by:

```bash
django-admin
```

The command should provide you with the help message, which recommend the useful subcommands for doing some action using `django-admin`.

## Create a Django Project

```bash
django-admin startproject monthly_challenges
```

After running the command, the below folder with this structure is created.

```text
monthly_challenges/
├── monthly_challenges/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## Start Development Server

```bash
python manage.py runserver
```

## Django Apps (Create an App)

```bash
python manage.py startapp challenges
```

After running the above command, a `challenges` folder is created, in the same level as `manage.py`, which contains:

```text
challenges/
├── migrations/
│   └── __init__.py
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

## Creating View and URL

In the `views.py` let's create a function (view).

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("This Works!")
```

Then, In our app, we need to make a connection between view function and the corresponding URL.
For this purpose, we create a python file `urls.py` next to `views.py` in the app we are working on.
Then, inside the `urls.py` file, we create a list as:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("january", views.index)
]
```

Then, we add the created URL of the `challenge` app in `monthly_challenges/urls.py` as:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path("challenges/", include("challenges/urls"))
]
```

`include("app_name.file_name")` is the file_name(without .py) in which URLs exist.
Without `/` it does not work!

### Dynamic Path

To define a **dynamic URL pattern**, add the following path in `challenges/urls.py`:

```python
urlpatterns = [
    path("<month>", views.monthly_challenges),
]
```

Next, define the corresponding view function in `challenges/views.py`:

```python
from django.http import HttpResponseNotFound

def monthly_challenges(request, month):
    challenge_text = None
    if month == "january":
        challenge_text = "Eat no meat for the entire month!"
    elif month == "febuary":
        challenge_text = "Do exercise for the entire month!"
    else:
        return HttpResponseNotFound("This month is not supported!")

    return HttpResponse(challenge_text)
```

#### More Specific Dynamic Path

```python
urlpatterns = [
    path("<int:month>", views.monthly_challenges),
]
```

or:

```python
urlpatterns = [
    path("<str:month>", views.monthly_challenges),
]
```

You can define both URL patterns, but the **order matters**.
The `<int:month>` path must be placed **before** the `<str:month>` path; otherwise, the string converter will match first, and the integer path will never be reached.
