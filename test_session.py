import app
app.app.testing = True
with app.app.test_client() as client:
    # Login first
    res = client.post('/login', data={'username': 'yosef', 'password': 'bcajember'})
    print("Login status:", res.status_code, res.headers.get('Location',''))
    
    # Now try DELETE
    res2 = client.delete('/api/bibliografi/10000')
    print("After login, delete status:", res2.status_code, res2.data.decode()[:100])
