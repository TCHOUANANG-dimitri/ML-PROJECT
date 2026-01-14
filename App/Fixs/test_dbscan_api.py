import json
import urllib.request

data = {
    'name': 'S001',
    'average': 14.5,
    'presence': 85,
    'projects': 2,
    'distance': '<5',
    'works': 'Non',
    'status': 'Admis'
}

req = urllib.request.Request(
    'http://localhost:8000/api/analyze/',
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print('Status: Success!' if result.get('success') else 'Status: Error')
        if result.get('analysis_cards'):
            print(f"Cluster ID: {result.get('cluster_id')}")
            print(f"Is Noise: {result.get('is_noise')}")
            print(f"Number of analysis cards: {len(result.get('analysis_cards', []))}")
            for i, card in enumerate(result.get('analysis_cards', [])[:2]):
                print(f"\nCard {i+1}: {card.get('title')}")
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
