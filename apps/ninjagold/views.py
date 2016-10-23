from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import random
import datetime

# Create your views here.
def index(request):
    if "currentGold" not in request.session or "log" not in request.session:
        request.session["currentGold"] = 0
        request.session["log"] = []
    return render(request, "ninjagold/index.html")

# @require_http_methods(["POST"]) # this decorator can setup what HTTP methods a view method accepts. however, if i tried a different method, I just got a blank page. might as well just do the if request.POST statment and redirect if needed
def process_money(request):
    if not request.POST:
        return redirect("/")
    if request.POST["location"] == "Farm":
        diceRoll = random.randrange(10, 21)
    elif request.POST["location"] == "Cave":
        diceRoll = random.randrange(5, 11)
    elif request.POST["location"] == "House":
        diceRoll = random.randrange(2, 6)
    elif request.POST["location"] == "Casino":
        diceRoll = random.choice([random.randrange(-50, 0), random.randrange(1, 51)])
    request.session["currentGold"] += diceRoll
    timeStamp = datetime.datetime.now().strftime("%m/%d/%Y %-I:%M %p")
    activity(request, diceRoll, request.POST["location"], timeStamp)
    return redirect("/")

def restart(request):
    if not request.POST:
        return redirect("/")
    # request.session.clear() # be careful, this may clear ALL session for every page you're browsing. Use ***del request.session["key"]***
    del request.session["log"]
    del request.session["currentGold"]
    return redirect("/")

def activity(request, diceRoll, location, timeStamp): # REMEMBER!: unlike Flask, "request" has to be explicitly set as a parameter. Otherwise, this function can't access session since no object with a session was passed to it!! In Flask, this was implicitly sent
    if diceRoll == -1 or diceRoll == 1:
        goldNumber = "gold"
    else:
        goldNumber = "golds"
    if diceRoll < 0:
        logEntry = "<p class='lostGold activity'>Entered a casino and lost "+str(diceRoll * -1)+" "+goldNumber+"... Ouch..</p>"+"<p class='activity timeStamp'>("+timeStamp+")</p><br>"
        request.session["log"].append(logEntry)
    else:
        logEntry = "<p class='wonGold activity'>Earned "+str(diceRoll)+" "+goldNumber+" from the "+location+"!</p>"+"<p class='activity timeStamp'>("+timeStamp+")</p><br>"
        request.session["log"].append(logEntry)
    # session["log"].insert(0, logEntry) // more efficient to append to end and print list last to first since we are printing list every time anyway
    # request.session["log"] = logEntry
    return
