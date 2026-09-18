from app import app
import json

client = app.test_client()

with app.test_request_context():
    # Attempt to post to /api/cetak_sirkulasi
    res = client.post('/api/cetak_sirkulasi', 
                      json={'ids': ['1', '2'], 'options': {'kartu': True, 'kantong': True}})
    print("Status:", res.status_code)
    if res.status_code != 200:
        print("Data:", res.data.decode('utf-8'))
