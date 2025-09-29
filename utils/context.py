def evaluate_risk_by_context(app_name, detections):
    app_name = app_name or "unknown"
    context = "unknown"

    if "csgo" in app_name or "valorant" in app_name or "steam" in app_name:
        context = "game"
    elif "chrome" in app_name or "edge" in app_name or "firefox" in app_name:
        context = "web"
    elif "whatsapp" in app_name or "telegram" in app_name or "discord" in app_name:
        context = "chat"
    elif "vlc" in app_name or "netflix" in app_name or "youtube" in app_name:
        context = "video"

    risk_score = 0
    if detections["weapon"]:
        risk_score += 1 if context == "game" else 3
    if detections["violence"]:
        risk_score += 3
    if detections["toxic"]:
        risk_score += 3 if context == "chat" else 1

    return context, risk_score
