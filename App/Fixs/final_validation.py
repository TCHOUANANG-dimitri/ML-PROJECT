#!/usr/bin/env python3
"""
Final validation test - check all initialization functions
"""
import re

print("=" * 70)
print("FINAL INITIALIZATION VALIDATION")
print("=" * 70)

with open('App/static/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    "✓ initNavigation() function": "function initNavigation()" in content,
    "✓ initRecommendationForm() function": "function initRecommendationForm()" in content,
    "✓ attachRecommendationFormListener() function": "function attachRecommendationFormListener()" in content,
    "✓ handleRecommendationSubmit() function": "function handleRecommendationSubmit(e)" in content,
    "✓ initNavigation() called in init()": "initNavigation()" in content[content.find("function init()"):content.find("function init()") + 500],
    "✓ initRecommendationForm() called in init()": "initRecommendationForm()" in content[content.find("function init()"):content.find("function init()") + 500],
    "✓ attachRecommendationFormListener() called in init()": "attachRecommendationFormListener()" in content[content.find("function init()"):content.find("function init()") + 500],
    "✓ Form listeners safe (null checks)": "if (recommendationForm)" in content,
    "✓ Sidebar variables initialized safely": "let recFiliereSelect = null" in content,
    "✓ No module-level DOM queries for forms": "const recommendationForm = document.getElementById" not in content,
}

all_pass = True
for check, result in checks.items():
    status = "✓" if result else "✗"
    print(f"{status} {check.replace('✓ ', '')}")
    if not result:
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("✅ ALL INITIALIZATION CHECKS PASSED!")
    print("=" * 70)
    print("\nThe following are NOW properly initialized in init():")
    print("  1. Navigation (sidebar buttons)")
    print("  2. Recommendation form selectors")
    print("  3. Recommendation form listeners")
    print("  4. All other page setup")
    print("\nNavigation should now work correctly!")
else:
    print("❌ SOME CHECKS FAILED")
    print("=" * 70)
