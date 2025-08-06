import re
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def analyze_code(code: str) -> dict:
    if not code.strip():
        return {
            "verdict": "Acidic",
            "score": -2,
            "feedback": ["Empty or whitespace-only code provided."]
        }
    
    score = 0
    feedback = []

    # Cyclomatic Complexity
    try:
        cc = cc_visit(code)
        avg_cc = sum([c.complexity for c in cc]) / len(cc) if cc else 0
        if avg_cc > 10:
            score -= 1
            feedback.append("High cyclomatic complexity.")
        elif avg_cc > 5:
            feedback.append("Moderate complexity.")
        else:
            score += 1
            feedback.append("Functions are clean.")
    except Exception:
        feedback.append("Could not analyze cyclomatic complexity.")

    # Maintainability Index
    try:
        mi = mi_visit(code, True)
        if mi < 50:
            score -= 1
            feedback.append("Low maintainability.")
        elif mi < 70:
            feedback.append("Average maintainability.")
        else:
            score += 1
            feedback.append("Good maintainability.")
    except Exception:
        feedback.append("Could not analyze maintainability index.")

    # Comments
    comments = len(re.findall(r'#', code))
    lines = len(code.splitlines())
    if lines > 0 and comments < lines * 0.1:
        score -= 1
        feedback.append("Too few comments.")
    else:
        score += 1
        feedback.append("Sufficient comments.")

    verdict = "Acidic" if score <= -1 else "Neutral" if score == 0 else "Basic"

    return {
        "verdict": verdict,
        "score": score,
        "feedback": feedback
    }
