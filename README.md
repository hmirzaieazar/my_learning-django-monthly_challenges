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
    path("<int:month>/", views.monthly_challenges_by_number),
]
```

or:

```python
urlpatterns = [
    path("<str:month>/", views.monthly_challenges),
]
```

You can define both URL patterns, but the **order matters**.
The `<int:month>` path must be placed **before** the `<str:month>` path; otherwise, the string converter will match first, and the integer path will never be reached.

### Giving a Name to a URL and Using the `reverse` Function for Redirection

First, assign a **name** to the URL pattern in `urls.py`. This allows Django to refer to the URL dynamically instead of hardcoding paths.

```python
urlpatterns = [
    path("<str:month>/", views.monthly_challenges, name="month-challenge"),
]
```

Next, use Django’s `reverse` function inside the view to generate the URL and redirect the user:

```python
def monthly_challenge_by_number(request, month):
    if month != 0 and month <= len(planned_challenges_of_month):
        months = list(planned_challenges_of_month.keys())
        redirected_month = months[month - 1]
        redirected_path = reverse(
            viewname="month-challenge",
            kwargs={"month": redirected_month},
        )
        return HttpResponseRedirect(redirected_path)
    else:
        return HttpResponseNotFound("The entered month is not valid!!!")
```

Using `reverse()` ensures that URLs are generated dynamically based on their name, making the code more maintainable and less error-prone if URL patterns change in the future.

## Django Templates

### Reading Template Files Using `render_to_string`

You can render an HTML template into a string using Django’s `render_to_string` function and return it as an HTTP response.

```python
from django.template.loader import render_to_string

def monthly_challenge(request, month):
    try:
        text_challenge = planned_challenges_of_month[month]
        html_response = render_to_string("challenges/challenge.html")
        return HttpResponse(html_response)
    except:
        return HttpResponseNotFound("The entered month is not valid!")
```

### Configuring Template Directories

Next, you need to tell Django where to find your template files. This configuration is done in `settings.py`.

Navigate to `monthly_challenges/settings.py`. There are two common approaches to configuring templates:

#### Recommended for Global Templates

This approach is useful when you want to store templates that are shared across multiple apps.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### Recommended for App-Specific Templates

This approach is ideal when each app manages its own templates.

Make sure that `APP_DIRS` is set to True, then place your templates inside the app’s templates directory (e.g., `challenges/templates/`).

```python
TEMPLATES = [
    {
        ...
        "DIRS": [],
        'APP_DIRS': True,
        ...
    },
]
```

Also, ensure that your app is registered in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "challenges",  # defined in challenges/apps.py
    ...
]
```

### Using Django’s `render` Shortcut

Instead of manually rendering a template to a string with `render_to_string`, Django provides the `render` shortcut, which combines template rendering and HTTP response creation in a single step.

This is the **recommended and cleaner approach**.

```python
from django.shortcuts import render
from django.http import HttpResponseNotFound

def monthly_challenge(request, month):
    try:
        text_challenge = planned_challenges_of_month[month]
        return render(
            request,
            "challenges/challenge.html",
            {"month": month, "month_challenge": text_challenge},
        )
    except:
        return HttpResponseNotFound("The entered month is not valid!")
```

## Django Template Language (DTL)

The **Django Template Language (DTL)** allows you to add logic and dynamic content to your HTML templates while keeping them clean and readable.

---

### Built-in Template Tags

Template tags control logic such as loops, conditions, URL generation, and template inheritance.

---

#### `for` Tag

Used to loop over a list or dictionary.

```html
<ul>
{% for month in months %}
    <li>{{ month }}</li>
{% endfor %}
</ul>
```

#### `if` Tag

Used to display content conditionally.

```html
{% if month_challenge is not None %}
    <h2>{{ month_challenge }}</h2>
{% else %}
    <h2>No challenge has been defined for this month!</h2>
{% endif %}
```

#### `url` Tag

Generates URLs dynamically using the name of a URL pattern.

```html
<a href="{% url "month-challenge" month=month %}">
```

This avoids hardcoding URLs and makes templates easier to maintain.

#### `block` Tag

The `{% block %}` tag is used with **template inheritance** to define sections of a template that child templates can override.

You can define **base (global) templates** inside: `BASE_DIR / "templates"`.

---

##### Base Template (`base.html`)

```html
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{% block title %}{% endblock %}</title>
    </head>
    <body>
        {% block body %}{% endblock %}
    </body>
</html>
```

This base template defines reusable blocks for the page title and body content.

---

##### Child Template (App Template)

Child templates extend the base template and override the defined blocks.

```html
{% extends "base.html" %}

{% block title %}Monthly Challenges{% endblock %}

{% block body %}
<ul>
    {% for month in months %}
        <li><a href="{% url "month-challenge" month=month %}">{{ month|title }}</a></li>
    {% endfor %}
</ul>
{% endblock %}
```

---

### Built-in Template Filters

#### `title` Filter

```html
<h1>{{ month|title }}</h1>
```
