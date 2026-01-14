import urllib.request
import json

# Test loading resources
url = "http://127.0.0.1:8000/api/load_resources/"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"✓ Loaded {len(data.get('rooms', []))} unique rooms")
        if data.get('rooms'):
            print(f"  First room: {data['rooms'][0]}")
except Exception as e:
    print(f"✗ Error loading resources: {e}")

# Test loading teachers
url = "http://127.0.0.1:8000/api/load_teachers/"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"✓ Loaded {len(data.get('teachers', []))} teachers")
        if data.get('teachers'):
            print(f"  First teacher: {data['teachers'][0]}")
except Exception as e:
    print(f"✗ Error loading teachers: {e}")
