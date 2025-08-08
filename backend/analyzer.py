"""
CodeLitmus - Advanced Code Quality Analyzer
Analyzes Python code for complexity, maintainability, and code quality metrics.
"""

import re
from radon.complexity import cc_visit
from radon.metrics import mi_visit


def analyze_code(code: str) -> dict:
    """
    Analyze code quality and return comprehensive metrics.
    
    Args:
        code (str): Source code to analyze
        
    Returns:
        dict: Analysis results with verdict, score, and detailed feedback
    """
    # Handle empty or whitespace-only code
    if not code.strip():
        return {
            "verdict": "Acidic",
            "verdict_explanation": "Code file is empty or contains only whitespace.",
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

    # Analyze Cyclomatic Complexity
    score, feedback, good_points, areas_for_improvement, metrics_explanation = _analyze_complexity(
        code, score, feedback, good_points, areas_for_improvement, metrics_explanation
    )
    
    # Analyze Maintainability Index
    score, feedback, good_points, areas_for_improvement, metrics_explanation = _analyze_maintainability(
        code, score, feedback, good_points, areas_for_improvement, metrics_explanation
    )
    
    # Analyze Comment Coverage
    score, feedback, good_points, areas_for_improvement, metrics_explanation = _analyze_comments(
        code, score, feedback, good_points, areas_for_improvement, metrics_explanation
    )

    # Ensure we have meaningful feedback
    if not areas_for_improvement:
        areas_for_improvement.append("Your code quality is excellent! Consider code reviews and continuous learning to maintain high standards.")
    
    if not good_points:
        good_points.append("Every codebase has potential - focus on the improvement areas to enhance quality.")

    # Determine verdict based on score
    verdict, verdict_explanation = _get_verdict(score)

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


def _analyze_complexity(code, score, feedback, good_points, areas_for_improvement, metrics_explanation):
    """Analyze cyclomatic complexity of the code."""
    try:
        cc = cc_visit(code)
        total_complexity = sum([c.complexity for c in cc])
        avg_cc = total_complexity / len(cc) if cc else 0
        function_count = len(cc)
        
        # Determine complexity status and color
        if avg_cc > 10:
            complexity_color = "#e74c3c"
            complexity_status = "⚠️ HIGH RISK"
            score -= 1
            feedback.append("High cyclomatic complexity detected.")
            areas_for_improvement.append(f"Reduce function complexity (average: {avg_cc:.1f}, ideal: <5)")
            explanation = f"<span style='color: {complexity_color}; font-weight: bold;'>{complexity_status}</span> - Your functions have <span style='color: {complexity_color}; font-weight: bold; font-size: 1.1em;'>{avg_cc:.1f}</span> average complexity. 🎯 <strong>Target: &lt;5 (Simple)</strong> | 📊 <strong>Scale: 1-5 (Simple) | 6-10 (Moderate) | 11+ (Complex)</strong>. Functions with complexity >10 are hard to test and maintain. Consider breaking down complex functions into smaller, single-purpose functions."
        elif avg_cc > 5:
            complexity_color = "#f39c12"
            complexity_status = "⚡ MODERATE"
            feedback.append("Moderate complexity detected.")
            areas_for_improvement.append(f"Consider simplifying some functions (average complexity: {avg_cc:.1f})")
            explanation = f"<span style='color: {complexity_color}; font-weight: bold;'>{complexity_status}</span> - Your code has <span style='color: {complexity_color}; font-weight: bold; font-size: 1.1em;'>{avg_cc:.1f}</span> average complexity. 🎯 <strong>Target: &lt;5 (Simple)</strong> | 📊 <strong>Scale: 1-5 (Simple) | 6-10 (Moderate) | 11+ (Complex)</strong>. While acceptable, aim for simpler functions for better readability and maintainability."
        else:
            complexity_color = "#27ae60"
            complexity_status = "✅ EXCELLENT"
            score += 1
            feedback.append("Functions are clean and simple.")
            good_points.append(f"Excellent function complexity! Average: {avg_cc:.1f} (target: <5)")
            explanation = f"<span style='color: {complexity_color}; font-weight: bold;'>{complexity_status}</span> - Your functions have <span style='color: {complexity_color}; font-weight: bold; font-size: 1.1em;'>{avg_cc:.1f}</span> average complexity. 🎯 <strong>Target: &lt;5 ✓</strong> | 📊 <strong>Scale: 1-5 (Simple) | 6-10 (Moderate) | 11+ (Complex)</strong>. This makes your code easy to understand, test, and maintain. Functions analyzed: {function_count}."
        
        metrics_explanation["complexity"] = explanation
        
    except Exception as e:
        feedback.append("Could not analyze cyclomatic complexity.")
        metrics_explanation["complexity"] = f"Analysis failed: {str(e)}. This might indicate syntax errors or unsupported language features."
    
    return score, feedback, good_points, areas_for_improvement, metrics_explanation


def _analyze_maintainability(code, score, feedback, good_points, areas_for_improvement, metrics_explanation):
    """Analyze maintainability index of the code."""
    try:
        mi = mi_visit(code, True)
        
        # Determine maintainability status and color
        if mi < 50:
            mi_color = "#e74c3c"
            mi_status = "❌ POOR"
            score -= 1
            feedback.append("Low maintainability index.")
            areas_for_improvement.append(f"Improve code maintainability (current: {mi:.1f}, target: >70)")
            explanation = f"<span style='color: {mi_color}; font-weight: bold;'>{mi_status}</span> - Maintainability Index: <span style='color: {mi_color}; font-weight: bold; font-size: 1.1em;'>{mi:.1f}/100</span>. 🎯 <strong>Target: &gt;70 (Good)</strong> | 📊 <strong>Scale: 0-49 (Poor) | 50-69 (Average) | 70-100 (Excellent)</strong>. Scores below 50 indicate code that's difficult to maintain. Consider: reducing complexity, improving variable names, adding comments, and breaking large functions into smaller ones."
        elif mi < 70:
            mi_color = "#f39c12"
            mi_status = "⚡ AVERAGE"
            feedback.append("Average maintainability.")
            areas_for_improvement.append(f"Good maintainability, but room for improvement (current: {mi:.1f}, target: >70)")
            explanation = f"<span style='color: {mi_color}; font-weight: bold;'>{mi_status}</span> - Maintainability Index: <span style='color: {mi_color}; font-weight: bold; font-size: 1.1em;'>{mi:.1f}/100</span>. 🎯 <strong>Target: &gt;70 (Good)</strong> | 📊 <strong>Scale: 0-49 (Poor) | 50-69 (Average) | 70-100 (Excellent)</strong>. Your code is reasonably maintainable but could benefit from clearer variable names, better structure, or additional comments."
        else:
            mi_color = "#27ae60"
            mi_status = "✅ EXCELLENT"
            score += 1
            feedback.append("Excellent maintainability.")
            good_points.append(f"High maintainability score: {mi:.1f}/100")
            explanation = f"<span style='color: {mi_color}; font-weight: bold;'>{mi_status}</span> - Maintainability Index: <span style='color: {mi_color}; font-weight: bold; font-size: 1.1em;'>{mi:.1f}/100</span>. 🎯 <strong>Target: &gt;70 ✓</strong> | 📊 <strong>Scale: 0-49 (Poor) | 50-69 (Average) | 70-100 (Excellent)</strong>. Your code is well-structured, readable, and easy to maintain. This suggests good naming conventions, appropriate complexity, and clear organization."
        
        metrics_explanation["maintainability"] = explanation
        
    except Exception as e:
        feedback.append("Could not analyze maintainability index.")
        metrics_explanation["maintainability"] = f"Analysis failed: {str(e)}. This might indicate syntax errors."
    
    return score, feedback, good_points, areas_for_improvement, metrics_explanation


def _analyze_comments(code, score, feedback, good_points, areas_for_improvement, metrics_explanation):
    """Analyze comment coverage in the code."""
    comments = len(re.findall(r'#', code))
    lines = len(code.splitlines())
    non_empty_lines = len([line for line in code.splitlines() if line.strip()])
    comment_ratio = comments / non_empty_lines if non_empty_lines > 0 else 0
    
    # Determine comment coverage status and color
    if comment_ratio < 0.1:
        comment_color = "#e74c3c"
        comment_status = "📝 NEEDS MORE"
        if lines > 0:
            score -= 1
            feedback.append("Insufficient comments.")
            areas_for_improvement.append(f"Add more comments ({comments} comments for {non_empty_lines} lines = {comment_ratio:.1%}, target: >10%)")
        explanation = f"<span style='color: {comment_color}; font-weight: bold;'>{comment_status}</span> - Comment coverage: <span style='color: {comment_color}; font-weight: bold; font-size: 1.1em;'>{comment_ratio:.1%}</span> (<span style='color: #3498db; font-weight: bold;'>{comments} comments</span> out of <span style='color: #9b59b6; font-weight: bold;'>{non_empty_lines} code lines</span>). 🎯 <strong>Target: &gt;10% (Good)</strong> | 📊 <strong>Scale: &lt;10% (Poor) | 10-20% (Good) | &gt;20% (Excellent)</strong>. Good code should have at least 10% comment coverage. Add comments to explain complex logic, function purposes, and important decisions."
    elif comment_ratio < 0.2:
        comment_color = "#f39c12"
        comment_status = "📝 DECENT"
        score += 1
        feedback.append("Good comment coverage.")
        good_points.append(f"Well-commented code: {comment_ratio:.1%} coverage ({comments} comments)")
        explanation = f"<span style='color: {comment_color}; font-weight: bold;'>{comment_status}</span> - Comment coverage: <span style='color: {comment_color}; font-weight: bold; font-size: 1.1em;'>{comment_ratio:.1%}</span> (<span style='color: #3498db; font-weight: bold;'>{comments} comments</span> out of <span style='color: #9b59b6; font-weight: bold;'>{non_empty_lines} code lines</span>). 🎯 <strong>Target: &gt;10% ✓</strong> | 📊 <strong>Scale: &lt;10% (Poor) | 10-20% (Good) | &gt;20% (Excellent)</strong>. Your code is well-documented, which helps other developers understand your logic and makes maintenance easier."
    else:
        comment_color = "#27ae60"
        comment_status = "📝 EXCELLENT"
        score += 1
        feedback.append("Excellent comment coverage.")
        good_points.append(f"Exceptionally well-commented code: {comment_ratio:.1%} coverage ({comments} comments)")
        explanation = f"<span style='color: {comment_color}; font-weight: bold;'>{comment_status}</span> - Comment coverage: <span style='color: {comment_color}; font-weight: bold; font-size: 1.1em;'>{comment_ratio:.1%}</span> (<span style='color: #3498db; font-weight: bold;'>{comments} comments</span> out of <span style='color: #9b59b6; font-weight: bold;'>{non_empty_lines} code lines</span>). 🎯 <strong>Target: &gt;20% ✓</strong> | 📊 <strong>Scale: &lt;10% (Poor) | 10-20% (Good) | &gt;20% (Excellent)</strong>. Your code is exceptionally well-documented. This level of documentation greatly improves code maintainability and team collaboration."
    
    metrics_explanation["comments"] = explanation
    
    return score, feedback, good_points, areas_for_improvement, metrics_explanation


def _get_verdict(score: int) -> tuple[str, str]:
    """
    Determine verdict based on score.
    
    Args:
        score (int): Overall quality score
        
    Returns:
        tuple: (verdict, verdict_explanation)
    """
    if score <= -2:
        return "Acidic", "Significant improvements needed"
    elif score == -1:
        return "Acidic", "Below average quality"
    elif score == 0:
        return "Neutral", "Average code quality"
    elif score == 1:
        return "Basic", "Good code quality"
    elif score == 2:
        return "Basic", "High code quality"
    else:  # score >= 3
        return "Basic", "Excellent code quality"
