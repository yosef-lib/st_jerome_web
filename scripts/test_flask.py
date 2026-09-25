from app import app
import json

app.config['TESTING'] = True
client = app.test_client()

response = client.post('/api/wa_webhook', json={
    'from': '6282257943768@c.us',
    'body': '2',
    'sender_name': 'Yosef Paskah'
})

print(response.status_code)
print(response.get_json())
