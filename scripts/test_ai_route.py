import json
import urllib.request
import urllib.parse

url = 'http://127.0.0.1:8037/api/ai/metadata'
data = {'query': 'Laskar Pelangi'}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
