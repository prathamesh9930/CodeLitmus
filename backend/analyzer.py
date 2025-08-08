import re
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def analyze_code(code: str) -> dict:
    if not code.strip():
        return {
            "verdict": "Acidic",
            "score": -3,
            "feedback": ["Empty or whitespace-only code provided."],
            "detailed_feedback": {
                "good_points": [],
                "areas_for_improvement": ["Code file is empty or contains only whitespace."],
                "metrics_explanation": {
                    "complexity": "Cannot analyze empty code.",
                    "maintainability": "Cannot analyze empty code.", 
                    "comments": "No code or comments found."
                }
            }
        }
    
    score = 0
    feedback = []
    good_points = []
    areas_for_improvement = []
    metrics_explanation = {}

    # Cyclomatic Complexity Analysis
    try:
        cc = cc_visit(code)
        total_complexity = sum([c.complexity for c in cc])
        avg_cc = total_complexity / len(cc) if cc else 0
        function_count = len(cc)
        
        # Color coding for complexity
        if avg_cc > 10:
            complexity_color = "#e74c3c"  # Red
            complexity_status = "⚠️ HIGH RISK"
        elif avg_cc > 5:
            complexity_color = "#f39c12"  # Orange/Yellow
            complexity_status = "⚡ MODERATE"
        else:
            complexity_color = "#27ae60"  # Green
            complexity_status = "✅ EXCELLENT"
        
        if avg_cc > 10:
            score -= 1
            feedback.append("High cyclomatic complexity detected.")
            areas_for_improvement.append(f"Reduce function complexity (average: {avg_cc:.1f}, ideal: <5)")
            metrics_explanation["complexity"] = f"<span style='color: {complexity_color}; font-weight: bold;'>{complexity_status}</span> - Your functions have <span style='color: {complexity_color}; font-weight: bold; font-size: 1.1em;'>{avg_cc:.1f}</span> average complexity. 🎯 <strong>Target: &lt;5 (Simple)</strong> | 📊 <strong>Scale: 1-5 (Simple) | 6-10 (Moderate) | 11+ (Complex)</strong>. Functions with complexity >10 are hard to test and maintain. Consider breaking down complex functions into smaller, single-purpose functions."
        elif avg_cc > 5:
            feedback.append("Moderate complexity detected.")
            areas_for_improvement.append(f"Consider simplifying some functions (average complexity: {avg_cc:.1f})")
            metrics_explanation["complexity"] = f"<span style='color: {complexity_color}; font-weight: bold;'>{complexity_status}</span> - Your code has <span style='color: {complexity_color}; font-weight: bold; font-size: 1.1em;'>{avg_cc:.1f}</span> average complexity. 🎯 <strong>Target: &lt;5 (Simple)</strong> | 📊 <strong>Scale: 1-5 (Simple) | 6-10 (Moderate) | 11+ (Complex)</strong>. While acceptable, aim for simpler functions for better readability and maintainability."
        else:
            score += 1
            feedback.append("Functions are clean and simple.")
            good_points.append(f"Excellent function complexity! Average: {avg_cc:.1f} (target: <5)")
            metrics_explanation["complexity"] = f"<span style='color: {complexity_color}; font-weight: bold;'>{complexity_status}</span> - Your functions have <span style='color: {complexity_color}; font-weight: bold; font-size: 1.1em;'>{avg_cc:.1f}</span> average complexity. 🎯 <strong>Target: &lt;5 ✓</strong> | 📊 <strong>Scale: 1-5 (Simple) | 6-10 (Moderate) | 11+ (Complex)</strong>. This makes your code easy to understand, test, and maintain. Functions analyzed: {function_count}."
    except Exception as e:
        feedback.append("Could not analyze cyclomatic complexity.")
        metrics_explanation["complexity"] = f"Analysis failed: {str(e)}. This might indicate syntax errors or unsupported language features."

    # Maintainability Index Analysis
    try:
        mi = mi_visit(code, True)
        
        # Color coding for maintainability
        if mi < 50:
            mi_color = "#e74c3c"  # Red
            mi_status = "❌ POOR"
        elif mi < 70:
            mi_color = "#f39c12"  # Orange/Yellow
            mi_status = "⚡ AVERAGE"
        else:
            mi_color = "#27ae60"  # Green
            mi_status = "✅ EXCELLENT"
        
        if mi < 50:
            score -= 1
            feedback.append("Low maintainability index.")
            areas_for_improvement.append(f"Improve code maintainability (current: {mi:.1f}, target: >70)")
            metrics_explanation["maintainability"] = f"<span style='color: {mi_color}; font-weight: bold;'>{mi_status}</span> - Maintainability Index: <span style='color: {mi_color}; font-weight: bold; font-size: 1.1em;'>{mi:.1f}/100</span>. 🎯 <strong>Target: &gt;70 (Good)</strong> | 📊 <strong>Scale: 0-49 (Poor) | 50-69 (Average) | 70-100 (Excellent)</strong>. Scores below 50 indicate code that's difficult to maintain. Consider: reducing complexity, improving variable names, adding comments, and breaking large functions into smaller ones."
        elif mi < 70:
            feedback.append("Average maintainability.")
            areas_for_improvement.append(f"Good maintainability, but room for improvement (current: {mi:.1f}, target: >70)")
            metrics_explanation["maintainability"] = f"<span style='color: {mi_color}; font-weight: bold;'>{mi_status}</span> - Maintainability Index: <span style='color: {mi_color}; font-weight: bold; font-size: 1.1em;'>{mi:.1f}/100</span>. 🎯 <strong>Target: &gt;70 (Good)</strong> | 📊 <strong>Scale: 0-49 (Poor) | 50-69 (Average) | 70-100 (Excellent)</strong>. Your code is reasonably maintainable but could benefit from clearer variable names, better structure, or additional comments."
        else:
            score += 1
            feedback.append("Excellent maintainability.")
            good_points.append(f"High maintainability score: {mi:.1f}/100")
            metrics_explanation["maintainability"] = f"<span style='color: {mi_color}; font-weight: bold;'>{mi_status}</span> - Maintainability Index: <span style='color: {mi_color}; font-weight: bold; font-size: 1.1em;'>{mi:.1f}/100</span>. 🎯 <strong>Target: &gt;70 ✓</strong> | 📊 <strong>Scale: 0-49 (Poor) | 50-69 (Average) | 70-100 (Excellent)</strong>. Your code is well-structured, readable, and easy to maintain. This suggests good naming conventions, appropriate complexity, and clear organization."
    except Exception as e:
        feedback.append("Could not analyze maintainability index.")
        metrics_explanation["maintainability"] = f"Analysis failed: {str(e)}. This might indicate syntax errors."

    # Comment Coverage Analysis
    comments = len(re.findall(r'#', code))
    lines = len(code.splitlines())
    non_empty_lines = len([line for line in code.splitlines() if line.strip()])
    comment_ratio = comments / non_empty_lines if non_empty_lines > 0 else 0
    
    # Color coding for comments
    if comment_ratio < 0.1:  # Less than 10%
        comment_color = "#e74c3c"  # Red
        comment_status = "📝 NEEDS MORE"
    elif comment_ratio < 0.2:  # 10-20%
        comment_color = "#f39c12"  # Orange/Yellow
        comment_status = "📝 DECENT"
    else:  # 20%+
        comment_color = "#27ae60"  # Green
        comment_status = "📝 EXCELLENT"
    
    if lines > 0 and comment_ratio < 0.1:
        score -= 1
        feedback.append("Insufficient comments.")
        areas_for_improvement.append(f"Add more comments ({comments} comments for {non_empty_lines} lines = {comment_ratio:.1%}, target: >10%)")
        metrics_explanation["comments"] = f"<span style='color: {comment_color}; font-weight: bold;'>{comment_status}</span> - Comment coverage: <span style='color: {comment_color}; font-weight: bold; font-size: 1.1em;'>{comment_ratio:.1%}</span> (<span style='color: #3498db; font-weight: bold;'>{comments} comments</span> out of <span style='color: #9b59b6; font-weight: bold;'>{non_empty_lines} code lines</span>). 🎯 <strong>Target: &gt;10% (Good)</strong> | 📊 <strong>Scale: &lt;10% (Poor) | 10-20% (Good) | &gt;20% (Excellent)</strong>. Good code should have at least 10% comment coverage. Add comments to explain complex logic, function purposes, and important decisions."
    else:
        score += 1
        feedback.append("Good comment coverage.")
        good_points.append(f"Well-commented code: {comment_ratio:.1%} coverage ({comments} comments)")
        metrics_explanation["comments"] = f"<span style='color: {comment_color}; font-weight: bold;'>{comment_status}</span> - Comment coverage: <span style='color: {comment_color}; font-weight: bold; font-size: 1.1em;'>{comment_ratio:.1%}</span> (<span style='color: #3498db; font-weight: bold;'>{comments} comments</span> out of <span style='color: #9b59b6; font-weight: bold;'>{non_empty_lines} code lines</span>). 🎯 <strong>Target: &gt;10% ✓</strong> | 📊 <strong>Scale: &lt;10% (Poor) | 10-20% (Good) | &gt;20% (Excellent)</strong>. Your code is well-documented, which helps other developers understand your logic and makes maintenance easier."

    # Additional code quality insights
    if not areas_for_improvement:
        areas_for_improvement.append("Your code quality is excellent! Consider code reviews and continuous learning to maintain high standards.")
    
    if not good_points:
        good_points.append("Every codebase has potential - focus on the improvement areas to enhance quality.")

    # Determine verdict with more nuanced descriptions
    if score <= -2:
        verdict = "Acidic"
        verdict_explanation = "Significant improvements needed"
    elif score == -1:
        verdict = "Acidic" 
        verdict_explanation = "Below average quality"
    elif score == 0:
        verdict = "Neutral"
        verdict_explanation = "Average code quality"
    elif score == 1:
        verdict = "Basic"
        verdict_explanation = "Good code quality"
    elif score == 2:
        verdict = "Basic"
        verdict_explanation = "High code quality"
    else:  # score >= 3
        verdict = "Basic"
        verdict_explanation = "Excellent code quality"

    return {
        "verdict": verdict,
        "verdict_explanation": verdict_explanation,
        "score": score,
        "feedback": feedback,
        "detailed_feedback": {
            "good_points": good_points,
            "areas_for_improvement": areas_for_improvement,
            "metrics_explanation": metrics_explanation
        }
    }
