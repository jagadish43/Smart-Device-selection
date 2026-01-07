import math
from urllib.parse import urlencode

from django.shortcuts import render
from apps.core.db import device_collection
from pymongo import ASCENDING, DESCENDING

BATTERY_OPTIONS = [1000, 2000, 3000, 4000, 5000, 6000]


def _to_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_text(value):
    if value is None:
        return None
    trimmed = str(value).strip()
    return trimmed if trimmed else None


def _brand_filter(value):
    if not value:
        return {}
    return {"brand": {"$regex": f"^{value}$", "$options": "i"}}


def _sorted_text_options(field, filters=None):
    query = filters or {}
    values = [
        str(value).strip()
        for value in device_collection.distinct(field, filter=query)
        if value is not None and str(value).strip()
    ]
    return sorted(set(values), key=lambda item: item.lower())


def _ram_storage_options(filters=None):
    base_match = {
        "ram": {"$exists": True, "$ne": None},
        "storage": {"$exists": True, "$ne": None},
    }
    match = {**base_match, **(filters or {})}
    pipeline = [
        {"$match": match},
        {"$group": {"_id": {"ram": "$ram", "storage": "$storage"}}},
    ]
    combos = []
    for doc in device_collection.aggregate(pipeline):
        ram_value = _to_int(doc.get("_id", {}).get("ram"))
        storage_value = _to_int(doc.get("_id", {}).get("storage"))
        if ram_value is None or storage_value is None:
            continue
        combos.append({"ram": ram_value, "storage": storage_value})
    return sorted(combos, key=lambda combo: (combo["ram"], combo["storage"]))


def _price_bounds(filters=None):
    def _bound(order):
        doc = device_collection.find_one(
            filter=filters or {},
            sort=[("price", order)],
            projection={"price": 1},
        )
        if not doc or doc.get("price") is None:
            return None
        return _to_int(doc.get("price"))

    min_price = _bound(ASCENDING) or 0
    max_price = _bound(DESCENDING) or 0
    if min_price > max_price:
        min_price, max_price = max_price, min_price
    return min_price, max_price


def home(request):
    page_param = request.GET.get("page", "1")
    page = _to_int(page_param, 1)
    if page is None or page < 1:
        page = 1

    limit = 10
    skip = (page - 1) * limit

    brand = _normalize_text(request.GET.get("brand"))
    battery = _to_int(request.GET.get("battery"))
    processor = _normalize_text(request.GET.get("processor"))
    display = _normalize_text(request.GET.get("display"))
    front_camera = _normalize_text(request.GET.get("front_camera"))
    back_camera = _normalize_text(request.GET.get("back_camera"))

    ram = _to_int(request.GET.get("ram"))
    storage = _to_int(request.GET.get("storage"))
    price_input = _to_int(request.GET.get("price"))

    brand_query = _brand_filter(brand)
    price_min, price_max = _price_bounds(brand_query)
    price_span = price_max - price_min
    price_step = max(1, price_span // 20) if price_span > 0 else 1
    if price_step < 100:
        price_step = 100

    selected_price = price_input if price_input is not None else price_max
    if selected_price is None:
        selected_price = price_max
    if price_min is not None and selected_price < price_min:
        selected_price = price_min
    if selected_price > price_max:
        selected_price = price_max

    query = dict(brand_query)
    if selected_price is not None:
        query["price"] = {"$lte": selected_price}
    if ram is not None:
        query["ram"] = ram
    if storage is not None:
        query["storage"] = storage
    if battery is not None:
        query["battery"] = {"$lte": battery}
    if processor:
        query["processor"] = {"$regex": processor, "$options": "i"}
    if display:
        query["display"] = {"$regex": display, "$options": "i"}
    if front_camera:
        query["front_camera"] = {"$regex": front_camera, "$options": "i"}
    if back_camera:
        query["rear_camera"] = {"$regex": back_camera, "$options": "i"}

    total_devices = device_collection.count_documents(query)
    total_pages = math.ceil(total_devices / limit) if total_devices else 1

    devices = list(
        device_collection.find(query)
        .skip(skip)
        .limit(limit)
    )

    pagination_params = {
        "brand": brand,
        "price": selected_price,
        "ram": ram,
        "storage": storage,
        "battery": battery,
        "processor": processor,
        "display": display,
        "front_camera": front_camera,
        "back_camera": back_camera,
    }
    sanitized_filters = {
        name: value
        for name, value in pagination_params.items()
        if value is not None and value != ""
    }
    pagination_query = urlencode(sanitized_filters)
    if pagination_query:
        pagination_query = f"&{pagination_query}"

    context = {
        "devices": devices,
        "current_page": page,
        "total_pages": total_pages,
        "brand": brand,
        "price": selected_price,
        "ram": ram,
        "storage": storage,
        "battery": battery,
        "processor": processor,
        "display": display,
        "front_camera": front_camera,
        "back_camera": back_camera,
        "brand_options": _sorted_text_options("brand"),
        "processor_options": _sorted_text_options("processor", brand_query),
        "display_options": _sorted_text_options("display", brand_query),
        "front_camera_options": _sorted_text_options("front_camera", brand_query),
        "back_camera_options": _sorted_text_options("rear_camera", brand_query),
        "battery_options": BATTERY_OPTIONS,
        "ram_storage_options": _ram_storage_options(brand_query),
        "price_min": price_min,
        "price_max": price_max,
        "price_step": price_step,
        "pagination_query": pagination_query,
    }

    return render(request, "home.html", context)
