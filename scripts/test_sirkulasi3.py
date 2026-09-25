from app import app
import json

app.config['TESTING'] = True
client = app.test_client()

with client.session_transaction() as sess:
    sess['logged_in'] = True
    sess['username'] = 'admin'

response = client.post('/api/sirkulasi/return', json={
    'book_id': '8037/22'
})

print(response.status_code)
print(response.get_data(as_text=True))
