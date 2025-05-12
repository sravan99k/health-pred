def calculate_risk(emotions, answers):
    emotion_score = sum([emotions.get(e, 0) for e in ['sad', 'angry', 'fear', 'disgust']])
    
    answer_score = 0
    scale = {"Always": 4, "Often": 3, "Sometimes": 2, "Rarely": 1, "Never": 0}
    for ans in answers.values():
        answer_score += scale.get(ans, 0)

    raw_risk = (emotion_score + answer_score)
    risk_percent = min(100, int(raw_risk * 3))  # scale factor

    return risk_percent
