import urllib.request
import json

url = "http://127.0.0.1:8000/api/program/"
payload = {
    "day": "Lundi",
    "slot": "AM",
    "teacher_id": 1,
    "room_id": 1,
    "filiere": "GIT",
    "niveau": 3,
    "matiere": "Algorithmique Avancée",
    "type": "CM",
    "effectif": 30,
    "date": "2026-01-14"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
