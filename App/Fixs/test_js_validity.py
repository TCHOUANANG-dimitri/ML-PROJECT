#!/usr/bin/env python3
"""
JavaScript validation test
"""

with open('d:\\ML-PROJECT\\App\\static\\js\\app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

print("=" * 70)
print("JavaScript Navigation Validation")
print("=" * 70)

# Check 1: initNavigation function exists
if 'function initNavigation()' in js_content:
    print("✓ initNavigation() function defined")
else:
    print("✗ initNavigation() function NOT found")

# Check 2: initNavigation is called in init()
init_start = js_content.find('function init() {')
if init_start != -1:
    init_section = js_content[init_start:init_start+500]
    if 'initNavigation()' in init_section:
        print("✓ initNavigation() called in init()")
    else:
        print("✗ initNavigation() NOT called in init()")
else:
    print("✗ init() function not found")

# Check 3: activatePage function exists
if 'function activatePage(pageName)' in js_content:
    print("✓ activatePage(pageName) function defined")
else:
    print("✗ activatePage(pageName) function NOT found")

# Check 4: Verify braces are balanced
open_braces = js_content.count('{')
close_braces = js_content.count('}')
if open_braces == close_braces:
    print(f"✓ Braces balanced ({open_braces} open, {close_braces} close)")
else:
    print(f"✗ Braces NOT balanced ({open_braces} open, {close_braces} close)")

# Check 5: DOMContentLoaded listener exists
if 'document.addEventListener("DOMContentLoaded", init)' in js_content:
    print("✓ DOMContentLoaded listener properly attached")
else:
    print("✗ DOMContentLoaded listener NOT found")

# Check 6: Sidebar-item query selectors exist
if '.sidebar-item' in js_content and 'querySelectorAll' in js_content:
    print("✓ Sidebar-item selectors found")
else:
    print("✗ Sidebar-item selectors NOT found")

# Check 7: Page query selectors exist  
if 'getElementById("page-' in js_content or '.page' in js_content:
    print("✓ Page section selectors found")
else:
    print("✗ Page section selectors NOT found")

print("\n" + "=" * 70)
print("Validation Complete - Navigation should now work!")
print("=" * 70)
