import app
app.app.testing = True
with app.app.test_client() as client:
    # Test WITHOUT login - should redirect
    res = client.delete('/api/bibliografi/10000')
    print("Without login:", res.status_code, res.headers.get('Location', ''))
    
    # Test WITH login
    with client.session_transaction() as sess:
        sess['logged_in'] = True
    res2 = client.delete('/api/bibliografi/10000')
    print("With login:", res2.status_code, res2.data.decode()[:100])
