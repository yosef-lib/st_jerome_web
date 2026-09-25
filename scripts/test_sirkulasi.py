from app import app
import json

app.config['TESTING'] = True
client = app.test_client()

response = client.post('/api/sirkulasi/return', json={
    'book_id': '8037/22'
})

print(response.status_code)
print(response.get_json())
