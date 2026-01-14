#!/usr/bin/env python
"""Test script to verify the API booking endpoint works correctly."""

import json
import requests
import time
import sys

# Wait for server to be ready
time.sleep(2)

BASE_URL = "http://127.0.0.1:8000"

def test_booking_valid():
    """Test a valid booking."""
    payload = {
        "day": "Lundi",
        "slot": "AM",
        "teacher_id": 1,
        "room_id": 1,
        "filiere": "GIT",
        "niveau": 3,
        "matiere": "Test Subject",
        "type": "CM",
        "effectif": 30,
        "date": "2026-01-14"
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/api/program/", json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        return resp.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_booking_missing_field():
    """Test with missing required field."""
    payload = {
        "day": "Lundi",
        "slot": "AM",
        "teacher_id": 1,
        # room_id missing
        "filiere": "GIT",
        "niveau": 3,
        "matiere": "Test",
        "type": "CM"
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/api/program/", json=payload, timeout=5)
        print(f"Status (missing field): {resp.status_code}")
        print(f"Response: {resp.text}")
        return resp.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing API booking endpoint...")
    
    results = []
    print("\n1. Testing valid booking:")
    results.append(("Valid booking", test_booking_valid()))
    
    print("\n2. Testing missing field:")
    results.append(("Missing field", test_booking_missing_field()))
    
    print("\n" + "="*50)
    print("Test Results:")
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    sys.exit(0 if all_passed else 1)
