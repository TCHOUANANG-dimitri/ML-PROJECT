#!/usr/bin/env python3
"""
Script to identify all module-level event listeners in app.js
"""
import re

with open('App/static/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find lines with addEventListener that are NOT inside functions
in_function = False
function_depth = 0

print("=" * 70)
print("MODULE-LEVEL EVENT LISTENERS (outside functions)")
print("=" * 70)

for i, line in enumerate(lines, 1):
    # Track function depth
    if re.search(r'function\s+\w+\s*\(', line):
        in_function = True
        function_depth += 1
    
    # Count braces
    function_depth += line.count('{') - line.count('}')
    
    # Check for addEventListener
    if 'addEventListener' in line and function_depth == 0:
        # Print context
        start = max(0, i-3)
        end = min(len(lines), i+3)
        
        print(f"\n📍 Line {i}:")
        for j in range(start, end):
            marker = ">>> " if j == i-1 else "    "
            print(f"{marker}{j+1:4d}: {lines[j].rstrip()}")
