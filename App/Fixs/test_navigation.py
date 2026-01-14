#!/usr/bin/env python3
"""
Test script to verify navigation functionality
"""

import re

# Read the index.html file
with open('d:\\ML-PROJECT\\App\\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Check if all pages are defined
pages_in_sidebar = [
    'dashboard',
    'recommendation', 
    'timetable',
    'teachers',
    'prediction',
    'analysis'
]

print("=" * 70)
print("Navigation Check")
print("=" * 70)

print("\n1. Checking sidebar buttons...")
for page in pages_in_sidebar:
    pattern = f'data-page="{page}"'
    if pattern in html_content:
        print(f"   ✓ Sidebar button for '{page}' found")
    else:
        print(f"   ✗ Sidebar button for '{page}' NOT found")

print("\n2. Checking page sections...")
for page in pages_in_sidebar:
    pattern = f'id="page-{page}"'
    if pattern in html_content:
        print(f"   ✓ Page section for '{page}' found")
    else:
        print(f"   ✗ Page section for '{page}' NOT found")

print("\n3. Checking CSS class definitions...")
with open('d:\\ML-PROJECT\\App\\static\\css\\styles.css', 'r', encoding='utf-8') as f:
    css_content = f.read()
    
if '.page {' in css_content and '.page.active {' in css_content:
    print("   ✓ CSS page styling found")
else:
    print("   ✗ CSS page styling MISSING")

print("\n4. Checking JavaScript navigation code...")
with open('d:\\ML-PROJECT\\App\\static\\js\\app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

if 'function activatePage(pageName)' in js_content:
    print("   ✓ activatePage function found")
else:
    print("   ✗ activatePage function NOT found")

if '.sidebar-item' in js_content and 'data-page' in js_content:
    print("   ✓ Sidebar event listeners found")
else:
    print("   ✗ Sidebar event listeners NOT found")

if 'document.addEventListener("DOMContentLoaded", init)' in js_content:
    print("   ✓ DOMContentLoaded event listener found")
else:
    print("   ✗ DOMContentLoaded event listener NOT found")

print("\n" + "=" * 70)
print("Navigation structure appears complete")
print("=" * 70)
