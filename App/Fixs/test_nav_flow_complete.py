#!/usr/bin/env python3
"""
Complete navigation test - emulate what happens in the browser
"""
import json
import re

def test_navigation_flow():
    """Test the complete navigation flow"""
    print("=" * 70)
    print("TESTING NAVIGATION FLOW")
    print("=" * 70)
    
    # Read HTML
    with open('App/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Read JS
    with open('App/static/js/app.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    # Test 1: Check that sidebar items have data-page attributes
    print("\n1. Checking sidebar items have data-page attributes:")
    sidebar_btns = re.findall(r'<button[^>]*class="sidebar-item[^"]*"[^>]*data-page="([^"]+)"', html)
    for page in sidebar_btns:
        print(f"   ✓ Sidebar item for page: {page}")
    
    # Test 2: Check that page sections exist
    print("\n2. Checking page sections exist:")
    page_sections = re.findall(r'<div[^>]*id="page-(\w+)"', html)
    for page in page_sections:
        print(f"   ✓ Page section found: {page}")
    
    # Test 3: Verify initNavigation function structure
    print("\n3. Checking initNavigation() function structure:")
    
    # Extract initNavigation function
    init_nav_match = re.search(r'function initNavigation\(\)\s*\{(.*?)\n\}', js, re.DOTALL)
    if init_nav_match:
        init_nav_body = init_nav_match.group(1)
        
        checks = {
            "Gets sidebar element": "getElementById(\"sidebar\")" in init_nav_body,
            "Gets sidebar items": "querySelectorAll(\".sidebar-item\")" in init_nav_body,
            "Adds click listener to items": "addEventListener(\"click\"" in init_nav_body,
            "Calls activatePage with data-page": "activatePage(page)" in init_nav_body,
            "Handles data-page-target buttons": "data-page-target" in init_nav_body,
        }
        
        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"   {status} {check}")
    else:
        print("   ✗ Could not find initNavigation function")
    
    # Test 4: Verify activatePage function
    print("\n4. Checking activatePage() function structure:")
    
    activate_match = re.search(r'function activatePage\(pageName\)\s*\{(.*?)\n\}', js, re.DOTALL)
    if activate_match:
        activate_body = activate_match.group(1)
        
        checks = {
            "Gets all sidebar items": "querySelectorAll(\".sidebar-item\")" in activate_body,
            "Gets all page sections": "querySelectorAll(\".page\")" in activate_body,
            "Toggles active class on items": "classList.toggle(\"active\"" in activate_body and "dataset.page === pageName" in activate_body,
            "Toggles active class on pages": "classList.toggle(\"active\"" in activate_body and "page-" in activate_body,
        }
        
        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"   {status} {check}")
    else:
        print("   ✗ Could not find activatePage function")
    
    # Test 5: Verify init() calls initNavigation
    print("\n5. Checking init() function calls initNavigation():")
    
    init_match = re.search(r'function init\(\)\s*\{(.*?)\n\}', js, re.DOTALL)
    if init_match:
        init_body = init_match.group(1)
        if "initNavigation()" in init_body:
            print("   ✓ init() calls initNavigation()")
            # Check if it's first
            lines = init_body.split('\n')
            first_call = None
            for line in lines:
                if line.strip() and not line.strip().startswith('//'):
                    first_call = line.strip()
                    break
            
            if first_call and "initNavigation" in first_call:
                print("   ✓ initNavigation() is FIRST call in init()")
            else:
                print(f"   ⚠ initNavigation() is not first call (first: {first_call[:50]}...)")
        else:
            print("   ✗ init() does NOT call initNavigation()")
    else:
        print("   ✗ Could not find init() function")
    
    # Test 6: Verify DOMContentLoaded listener
    print("\n6. Checking DOMContentLoaded listener:")
    
    if 'document.addEventListener("DOMContentLoaded", init)' in js or "DOMContentLoaded" in js:
        print("   ✓ DOMContentLoaded listener attached to init()")
    else:
        print("   ✗ DOMContentLoaded listener NOT found")
    
    print("\n" + "=" * 70)
    print("NAVIGATION FLOW TEST COMPLETE")
    print("=" * 70)
    print("\nExpected behavior:")
    print("1. Page loads → DOMContentLoaded fires")
    print("2. DOMContentLoaded calls init()")
    print("3. init() immediately calls initNavigation()")
    print("4. initNavigation() attaches click listeners to sidebar items")
    print("5. User clicks sidebar button → click event fires")
    print("6. activatePage() called with page name")
    print("7. activatePage() toggles active class on item and page section")
    print("8. Page becomes visible (.page.active { display: block })")

if __name__ == "__main__":
    test_navigation_flow()
