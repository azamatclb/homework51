from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render
from webapp.cat_db import CatDb


def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        name = request.POST.get("name")
        CatDb.cat_statistic = {
            "name": name,
            "age": 1,
            "happiness": 40,
            "satiety": 40,
            "is_sleeping": False
        }
        return HttpResponseRedirect("/cat_stats")


def cat_stats(request):
    cat = CatDb.cat_statistic

    if request.method == "POST":
        action = request.POST.get("actions")
        if action == "feed":
            feed_cat(cat)
        elif action == "play":
            play_with_cat(cat)
        elif action == "sleep":
            sleep_cat(cat)
        return HttpResponseRedirect("/cat_stats")

    return render(request, "cat_stats.html", context={"cat": cat})


def feed_cat(cat):
    if not cat["is_sleeping"]:
        cat["satiety"] = min(100, cat["satiety"] + 15)
        cat["happiness"] = min(100, cat["happiness"] + 5)
        if cat["satiety"] > 100:
            cat["happiness"] = max(0, cat["happiness"] - 30)


def play_with_cat(cat):
    if cat["is_sleeping"]:
        cat["happiness"] = max(0, cat["happiness"] - 5)
        cat["is_sleeping"] = False
    else:
        if randint(1, 3) == 1:
            cat["happiness"] = 0
        else:
            cat["happiness"] = min(100, cat["happiness"] + 15)
        cat["satiety"] = max(0, cat["satiety"] - 10)


def sleep_cat(cat):
    cat["is_sleeping"] = True
