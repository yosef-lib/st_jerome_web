from app import app
import json

app.config['LOGIN_DISABLED'] = True

client = app.test_client()
res = client.post('/api/cetak_sirkulasi', 
                  json={'ids': ['1', '2'], 'options': {'kartu': True, 'kantong': True}})
print("Status:", res.status_code)
if res.status_code != 200:
    print("Data:", res.data.decode('utf-8'))
