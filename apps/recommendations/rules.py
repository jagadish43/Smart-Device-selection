def calculate_score(device, user_pref):
    score = 0

    # Budget rule
    if device.get("price", 0) <= user_pref["budget"]:
        score += 30

    # Brand rule (case-insensitive)
    if device.get("brand", "").lower() in user_pref["brands"]:
        score += 20

    # Usage rules
    usage = user_pref["usage"]

    if usage == "Gaming":
        if device.get("ram", 0) >= 8:
            score += 25
        if "120hz" in device.get("display", "").lower():
            score += 10

    if usage == "Camera":
        if "mp" in device.get("rear_camera", "").lower():
            score += 25

    if usage == "Battery":
        if device.get("battery") and "5000" in str(device["battery"]):
            score += 25

    return score


def recommend_devices(devices, user_pref):
    results = []

    for device in devices:
        device["score"] = calculate_score(device, user_pref)
        results.append(device)

    return sorted(results, key=lambda x: x["score"], reverse=True)
