import urllib.request
import json

url = "http://127.0.0.1:8000/api/program/"
payload = {
    "day": "Mercredi",
    "slot": "PM",
    "teacher_id": 2,
    "room_id": 2,
    "filiere": "GIT",
    "niveau": 3,
    "matiere": "Algorithmique Avancée",
    "type": "CM",
    "effectif": 50,
    "date": "2026-01-16"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}")
    print(f"Error: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
