#!/usr/bin/env python3
"""
Debug script to check navigation functionality
"""
import re
import sys

def check_app_js():
    """Check if navigation functions are properly defined"""
    print("=" * 60)
    print("CHECKING APP.JS NAVIGATION SETUP")
    print("=" * 60)
    
    with open('App/static/js/app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "initNavigation() defined": "function initNavigation()" in content,
        "activatePage() defined": "function activatePage(pageName)" in content,
        "initNavigation() called in init()": "initNavigation()" in content[content.find("function init()"):],
        "DOMContentLoaded listener": 'document.addEventListener("DOMContentLoaded"' in content,
        "querySelector for sidebar-item": '.sidebar-item' in content,
        "data-page attribute handling": 'btn.dataset.page' in content,
    }
    
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    all_pass = all(checks.values())
    print(f"\nResult: {'PASS' if all_pass else 'FAIL'}")
    return all_pass

def check_html():
    """Check if HTML has required navigation elements"""
    print("\n" + "=" * 60)
    print("CHECKING INDEX.HTML NAVIGATION ELEMENTS")
    print("=" * 60)
    
    with open('App/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all sidebar items
    sidebar_items = re.findall(r'data-page="(\w+)"', content)
    print(f"Found {len(sidebar_items)} sidebar items: {sidebar_items}")
    
    # Check for page sections
    page_sections = re.findall(r'id="page-(\w+)"', content)
    print(f"Found {len(page_sections)} page sections: {page_sections}")
    
    # Check CSS styles
    css_checks = {
        "sidebar exists": 'id="sidebar"' in content,
        "sidebar-item class": 'class="sidebar-item' in content,
        "page-dashboard section": 'id="page-dashboard"' in content,
        "page-recommendation section": 'id="page-recommendation"' in content,
    }
    
    print("\nHTML Elements:")
    for check, result in css_checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    all_pass = all(css_checks.values())
    print(f"\nResult: {'PASS' if all_pass else 'FAIL'}")
    return all_pass

def check_css():
    """Check if CSS has required styles"""
    print("\n" + "=" * 60)
    print("CHECKING STYLES.CSS")
    print("=" * 60)
    
    with open('App/static/css/styles.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    css_checks = {
        ".page { display: none }": ".page" in content and "display: none" in content,
        ".page.active { display: block }": ".page.active" in content and "display: block" in content,
        ".sidebar-item": ".sidebar-item" in content,
    }
    
    for check, result in css_checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    all_pass = all(css_checks.values())
    print(f"\nResult: {'PASS' if all_pass else 'FAIL'}")
    return all_pass

def check_file_structure():
    """Check that all required files exist"""
    print("\n" + "=" * 60)
    print("CHECKING FILE STRUCTURE")
    print("=" * 60)
    
    import os
    
    files = {
        "App/index.html": os.path.exists("App/index.html"),
        "App/static/js/app.js": os.path.exists("App/static/js/app.js"),
        "App/static/css/styles.css": os.path.exists("App/static/css/styles.css"),
        "App/manage.py": os.path.exists("App/manage.py"),
    }
    
    for file, exists in files.items():
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
    
    all_pass = all(files.values())
    print(f"\nResult: {'PASS' if all_pass else 'FAIL'}")
    return all_pass

if __name__ == "__main__":
    js_ok = check_app_js()
    html_ok = check_html()
    css_ok = check_css()
    files_ok = check_file_structure()
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    if all([js_ok, html_ok, css_ok, files_ok]):
        print("✓ All checks passed! Navigation setup is complete.")
        print("\nNext steps:")
        print("1. Start Django server: python App/manage.py runserver")
        print("2. Open browser to http://127.0.0.1:8000/")
        print("3. Press F12 and check Console for any errors")
        print("4. Try clicking sidebar buttons")
    else:
        print("✗ Some checks failed. See above for details.")
        sys.exit(1)
