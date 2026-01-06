from django.shortcuts import render
from apps.core.db import device_collection
import math

def home(request):
    # Pagination
    page = int(request.GET.get("page", 1))
    limit = 10
    skip = (page - 1) * limit

    # ===== USER FILTERS =====
    brand = request.GET.get("brand")
    max_price = request.GET.get("price")

    query = {}

    if brand:
        query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}

    if max_price:
        query["price"] = {"$lte": int(max_price)}

    # ===== COUNT & FETCH =====
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
        "brand": brand,
        "price": max_price,
    }

    return render(request, "home.html", context)
