from django.shortcuts import render
from apps.core.db import device_collection
import math

def home(request):
    page = int(request.GET.get("page", 1))
    limit = 10
    skip = (page - 1) * limit

    # ===== GET FILTER VALUES =====
    brand = request.GET.get("brand")
    max_price = request.GET.get("price")
    ram = request.GET.get("ram")
    storage = request.GET.get("storage")
    battery = request.GET.get("battery")
    processor = request.GET.get("processor")
    display = request.GET.get("display")
    front_camera = request.GET.get("front_camera")
    back_camera = request.GET.get("back_camera")

    # ===== BUILD MONGO QUERY =====
    query = {}

    if brand:
        query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}

    if max_price:
        query["price"] = {"$lte": int(max_price)}

    if ram:
        query["ram"] = int(ram)

    if storage:
        query["storage"] = int(storage)

    if battery:
        query["battery"] = {"$regex": battery, "$options": "i"}

    if processor:
        query["processor"] = {"$regex": processor, "$options": "i"}

    if display:
        query["display"] = {"$regex": display, "$options": "i"}

    if front_camera:
        query["front_camera"] = {"$regex": front_camera, "$options": "i"}

    if back_camera:
        query["rear_camera"] = {"$regex": back_camera, "$options": "i"}

    # ===== PAGINATION =====
    total_devices = device_collection.count_documents(query)
    total_pages = math.ceil(total_devices / limit)

    devices = list(
        device_collection.find(query)
        .skip(skip)
        .limit(limit)
    )

    context = {
        "devices": devices,
        "current_page": page,
        "total_pages": total_pages,

        # keep filter values
        "brand": brand,
        "price": max_price,
        "ram": ram,
        "storage": storage,
        "battery": battery,
        "processor": processor,
        "display": display,
        "front_camera": front_camera,
        "back_camera": back_camera,
    }

    return render(request, "home.html", context)
