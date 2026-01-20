from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

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
        return HttpResponse(f"Challenge of {month} is {text_challenge}")
    except:
        return HttpResponseNotFound("The entered month is not valid!")
