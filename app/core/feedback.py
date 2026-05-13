def generate_feedback(results):
    feedback = []
    wrong_count = 0
    missing_count = 0
    extra_count = 0
    similar_count = 0
    accent_count = 0
    correct_count = 0

    for r in results:
        if r["type"] == "correct":
            correct_count += 1
        elif r["type"] == "accent_match":
            accent_count += 1
        elif r["type"] == "similar":
            similar_count += 1
        elif r["type"] == "wrong":
            wrong_count += 1
        elif r["type"] == "missing":
            missing_count += 1
        elif r["type"] == "extra":
            extra_count += 1

    total = len(results)
    if total == 0:
        return ["No audio detected. Please try again."]

    accuracy = (correct_count + accent_count) / total

    # Overall assessment
    if accuracy >= 0.9:
        feedback.append("Excellent pronunciation! Almost perfect.")
    elif accuracy >= 0.7:
        feedback.append("Good pronunciation overall. Minor improvements possible.")
    elif accuracy >= 0.5:
        feedback.append("Fair attempt. Keep practicing the highlighted sounds.")
    else:
        feedback.append("Needs improvement. Focus on the red-marked sounds below.")

    # Accent note
    if accent_count > 0:
        feedback.append(f"{accent_count} sound(s) matched your accent pattern — counted as correct.")

    # Specific issues
    if similar_count > 0:
        feedback.append(f"{similar_count} sound(s) were close but not exact — practice clarity.")

    if wrong_count > 0:
        # Collect specific wrong pairs
        wrong_pairs = [(r["expected"], r["spoken"]) for r in results if r["type"] == "wrong" and r["expected"] and r["spoken"]]
        if wrong_pairs:
            tips = [f'"{exp}" → you said "{spk}"' for exp, spk in wrong_pairs[:3]]
            feedback.append("Focus on: " + ", ".join(tips))

    if missing_count > 0:
        missed = [r["expected"] for r in results if r["type"] == "missing" and r["expected"]]
        if missed:
            feedback.append(f"You missed {missing_count} sound(s): {', '.join(missed[:3])}")

    if extra_count > 0:
        feedback.append(f"{extra_count} extra sound(s) detected — try to be more precise.")

    return feedback