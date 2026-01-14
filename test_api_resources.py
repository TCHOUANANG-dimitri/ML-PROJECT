import urllib.request
import json
import sys

try:
    url = "http://127.0.0.1:8000/api/load_resources/"
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        rooms_count = len(data.get('rooms', []))
        print(f"SUCCESS: Loaded {rooms_count} unique rooms from API")
        if rooms_count > 0:
            r = data['rooms'][0]
            print(f"  Sample room: id={r['id']}, name={r['name']}, capacity={r['capacity']}")
except urllib.error.URLError as e:
    print(f"Connection error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    url = "http://127.0.0.1:8000/api/load_teachers/"
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        teachers_count = len(data.get('teachers', []))
        print(f"SUCCESS: Loaded {teachers_count} teachers from API")
        if teachers_count > 0:
            t = data['teachers'][0]
            print(f"  Sample teacher: id={t['id']}, name={t['name']}, dept={t['department']}")
except Exception as e:
    print(f"Error loading teachers: {e}")
    sys.exit(1)

print("\nAll API tests passed!")
