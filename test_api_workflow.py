import urllib.request
import json

def test_api():
    """Test complete booking workflow."""
    url = "http://127.0.0.1:8000/api/program/"
    
    test_cases = [
        {
            "name": "Valid booking",
            "payload": {
                "day": "Lundi",
                "slot": "AM",
                "teacher_id": 1,
                "room_id": 1,
                "filiere": "GIT",
                "niveau": 3,
                "matiere": "Algorithmique Avancée",
                "type": "CM",
                "effectif": 50,
                "date": "2026-01-14"
            },
            "expect_status": 200,
            "description": "Should succeed with valid data"
        },
        {
            "name": "Duplicate slot",
            "payload": {
                "day": "Lundi",
                "slot": "AM",
                "teacher_id": 2,
                "room_id": 1,
                "filiere": "GIT",
                "niveau": 3,
                "matiere": "Test",
                "type": "CM",
                "effectif": 30,
                "date": "2026-01-14"
            },
            "expect_status": 400,
            "description": "Should fail - room already booked for this slot"
        },
        {
            "name": "Capacity exceeded",
            "payload": {
                "day": "Mardi",
                "slot": "PM",
                "teacher_id": 1,
                "room_id": 3,
                "filiere": "GIT",
                "niveau": 3,
                "matiere": "Test",
                "type": "CM",
                "effectif": 100,
                "date": "2026-01-15"
            },
            "expect_status": 400,
            "description": "Should fail - class size exceeds room capacity"
        }
    ]
    
    for test in test_cases:
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(test["payload"]).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            try:
                with urllib.request.urlopen(req) as response:
                    status = response.status
                    body = json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                status = e.code
                body = json.loads(e.read().decode('utf-8'))
            
            passed = status == test["expect_status"]
            symbol = "✓" if passed else "✗"
            print(f"{symbol} {test['name']}: {test['description']}")
            print(f"   Status: {status} (expected {test['expect_status']})\n")
        except Exception as e:
            print(f"✗ {test['name']}: ERROR - {e}\n")

if __name__ == "__main__":
    test_api()
