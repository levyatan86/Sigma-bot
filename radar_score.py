# radar_score.py

def score_trade(data):
    score = 0
    reasons = []

    # ✅ Direction present
    if data.get("direction") in ["long", "short"]:
        score += 1
        reasons.append("Has direction")

    # 🔄 Structure notes
    structure_notes = data.get("notes", "").lower()
    if any(word in structure_notes for word in ["break", "sweep", "retest"]):
        score += 2
        reasons.append("Structure logic")

    # ⏰ Session timing
    if data.get("session", "").lower() in ["london", "new york"]:
        score += 1
        reasons.append("High-liquidity session")

    # 😎 Trader confidence
    if data.get("emotion", "").lower() in ["confident", "clear"]:
        score += 1
        reasons.append("Trader confident")

    # 📊 Volume mention
    if "volume" in structure_notes:
        score += 1
        reasons.append("Volume mentioned")

    # Normalize to 10-point scale
    final_score = round((score / 6) * 10, 1)
    return final_score, reasons
