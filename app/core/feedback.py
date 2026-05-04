def generate_feedback(results):
    feedback = []

    for r in results:
        if r["type"] == "wrong":
            feedback.append("Sound not clear")
        elif r["type"] == "missing":
            feedback.append("You missed a sound")
        elif r["type"] == "extra":
            feedback.append("Extra sound detected")

    if not feedback:
        feedback.append("Good pronunciation")

    return feedback