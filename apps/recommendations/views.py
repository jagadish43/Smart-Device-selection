from django.shortcuts import render
from apps.core.db import device_collection
from .rules import recommend_devices

def recommend_view(request):
    if request.method == "POST":
        user_pref = {
            "budget": int(request.POST["budget"]),
            "brands": [b.lower() for b in request.POST.getlist("brands")],
            "usage": request.POST["usage"],
        }

        devices = list(device_collection.find())
        results = recommend_devices(devices, user_pref)

        return render(request, "results.html", {"devices": results})

    return render(request, "home.html")
