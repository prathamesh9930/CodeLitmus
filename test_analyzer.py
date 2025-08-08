#!/usr/bin/env python3
"""
Test script for CodeLitmus analyzer functionality.
Tests the code analysis capabilities with sample code snippets.
"""

import sys
import os

# Add backend directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.analyzer import analyze_code


def test_excellent_code():
    """Test analyzer with high-quality code."""
    excellent_code = '''
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number using dynamic programming.
    
    Args:
        n (int): Position in Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 1:
        return n
    
    # Use dynamic programming for efficiency
    prev, curr = 0, 1
    
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def validate_input(value):
    """Validate that input is a non-negative integer.
    
    Args:
        value: Input value to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return isinstance(value, int) and value >= 0
'''
    
    result = analyze_code(excellent_code)
    print("🧪 Testing Excellent Code:")
    print(f"Verdict: {result['verdict']}")
    print(f"Score: {result['score']}")
    print(f"Explanation: {result['verdict_explanation']}")
    print("-" * 50)


def test_poor_code():
    """Test analyzer with poor-quality code."""
    poor_code = '''
def bad_function(a,b,c,d,e):
    if a>0:
        if b>0:
            if c>0:
                if d>0:
                    if e>0:
                        return a+b+c+d+e
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    else:
        return 0

def x(y):
    return y*2
'''
    
    result = analyze_code(poor_code)
    print("🧪 Testing Poor Code:")
    print(f"Verdict: {result['verdict']}")
    print(f"Score: {result['score']}")
    print(f"Explanation: {result['verdict_explanation']}")
    print("-" * 50)


def test_empty_code():
    """Test analyzer with empty code."""
    result = analyze_code("")
    print("🧪 Testing Empty Code:")
    print(f"Verdict: {result['verdict']}")
    print(f"Score: {result['score']}")
    print(f"Explanation: {result['verdict_explanation']}")
    print("-" * 50)


if __name__ == "__main__":
    print("🚀 CodeLitmus Analyzer Test Suite")
    print("=" * 50)
    
    test_excellent_code()
    test_poor_code()
    test_empty_code()
    
    print("✅ All tests completed!")
