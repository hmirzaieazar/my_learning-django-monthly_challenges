from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

# Create your views here.

planned_challenges_of_month = {
    "january": "A",
    "febuary": "B",
    "march": "C",
    "april": "D",
    "may": "E",
    "june": "F",
    "july": "G",
    "august": "H",
    "september": "I",
    "october": "J",
    "november": "K",
    "december": "L",
}


def index(request):
    response = ""
    for month in planned_challenges_of_month:
        ref_path = reverse("month-challenge", kwargs={"month": month})
        response += f"<li><a href='{ref_path}'>{month}</a></li>"
    return HttpResponse(f"<ul>{response}</ul>")


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


def monthly_challenge(request, month):
    try:
        text_challenge = planned_challenges_of_month[month]
        # return HttpResponse(f"Challenge of {month} is {text_challenge}")
        html_response = render_to_string("challenges/challenge.html")
        return HttpResponse(html_response)
    except:
        return HttpResponseNotFound("The entered month is not valid!")
