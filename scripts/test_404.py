from app import app

app.config['TESTING'] = True
client = app.test_client()

with client.session_transaction() as sess:
    sess['logged_in'] = True
    sess['username'] = 'admin'

response = client.get('/api/sirkulasi/member/9037%2F22')
print("Status:", response.status_code)
print("Data:", response.get_data(as_text=True)[:200])
